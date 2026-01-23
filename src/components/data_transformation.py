import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from src.constants.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS
from src.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from src.components.data_validation import DataValidation
from src.entity.config_entity import DataTransformationConfig
from src.utils.main_utils.utils import save_numpy_arr_data,save_pkl_obj

from src.exception.exception import CustomException
from src.logging.logger import logging

class DataTransformation:
    def __init__(self,data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise CustomException(e,sys)

    def get_data_transformer_obj(self)->Pipeline:
        logging.info("Entered (get_data_transformer_obj)")
        try:
            knn_imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("KNN Imputer initialized (get_data_transformer_obj)")
            preprocessor = Pipeline([("imputer",knn_imputer)])
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifact:
        logging.info("Entered Data Transformation (initiate_data_transformation)")
        try:
            logging.info("Starting Data Transformation (initiate_data_transformation)")
            train_df = DataValidation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataValidation.read_data(self.data_validation_artifact.valid_test_file_path)


            input_feature_train_df = train_df.drop(TARGET_COLUMN,axis=1)
            input_feature_test_df = test_df.drop(TARGET_COLUMN,axis=1)

            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_test_df = test_df[TARGET_COLUMN]

            target_feature_train_df = target_feature_train_df.apply(lambda x: 0 if x == -1 else x)
            target_feature_test_df = target_feature_test_df.apply(lambda x: 0 if x == -1 else x)

            preprocessor = self.get_data_transformer_obj()
            transformed_input_train_features = preprocessor.fit_transform(input_feature_train_df)
            transformed_input_test_features = preprocessor.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_features,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_features,np.array(target_feature_test_df)]

            save_numpy_arr_data(
                self.data_transformation_config.transformed_train_file_path,arr=train_arr
            )
            save_numpy_arr_data(
                self.data_transformation_config.transformed_test_file_path,arr=test_arr
            )
            save_pkl_obj(
                self.data_transformation_config.transformed_obj_file_path,obj=preprocessor
            )
            data_transformation_artifact = DataTransformationArtifact(
                transformed_obj_file_path=self.data_transformation_config.transformed_obj_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)

