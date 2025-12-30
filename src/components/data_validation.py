import os
import sys
import pandas as pd
from scipy.stats import ks_2samp

from src.exception.exception import CustomException
from src.logging.logger import logging
from src.components.data_ingestion import DataIngestion
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import DataIngestionConfig
from src.entity.config_entity import DataValidationConfig
from src.utils.main_utils.utils import read_yaml_file,write_yaml_file
from src.constants.training_pipeline import SCHEMA_FILE_PATH

class DataValidation:
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e,sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)

    def validate_number_of_columns(self,dataframe: pd.DataFrame)->bool:
        try:
            required_columns = self._schema_config["columns"]
            number_of_columns = len(required_columns)
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe has {len(dataframe.columns)} number of columns")

            if len(dataframe.columns) == number_of_columns:
                return True
            else:
                return False
        except Exception as e:
            raise CustomException(e,sys)

    def validate_numerical_columns(self,dataframe: pd.DataFrame)->bool:
        try:
            numerical_columns = self._schema_config["numerical_columns"]
            status = True
            missing_columns = []
            non_numerical_columns = []
            for column in numerical_columns:
                if column not in dataframe.columns:
                    status = False
                    missing_columns.append(column)
                else:
                    if not pd.api.types.is_numeric_dtype(dataframe[column]):
                        status = False
                        non_numerical_columns.append(column)
            if not status:
                logging.info(f"Missing columns: {missing_columns}")
                logging.info(f"Non-numerical columns: {non_numerical_columns}")
            return status
        except Exception as e:
            raise CustomException(e,sys)

    def detect_dataset_drift(self,base_df,curr_df,threshold=0.05):
        try:
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = curr_df[column]
                ks = ks_2samp(d1,d2)
                if threshold < ks.pvalue:
                    is_drift = False
                else:
                    is_drift = True
                report.update({column:{
                    "p_value": float(ks.pvalue),
                    "drift_status": is_drift
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)

        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            logging.info("Reading the data from train and test paths")
            train_data = DataValidation.read_data(train_file_path)
            test_data = DataValidation.read_data(test_file_path)

            status = self.validate_number_of_columns(dataframe=train_data)
            if not status:
                error_message = f"Train dataframe does not contain required number of columns.\n"
                raise Exception(error_message)
            status = self.validate_number_of_columns(dataframe=test_data)
            if not status:
                error_message = f"Test dataframe does not contain required number of columns.\n"
                raise Exception(error_message)
            status = self.validate_numerical_columns(dataframe=train_data)
            if not status:
                error_message = f"Train dataframe numerical column validation failed.\n"
                raise Exception(error_message)
            status = self.validate_numerical_columns(dataframe=test_data)
            if not status:
                error_message = f"Test dataframe numerical column validation failed.\n"
                raise Exception(error_message)

            status = self.detect_dataset_drift(base_df=train_data,curr_df=test_data)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok=True)

            train_data.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)
            test_data.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)

            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)





