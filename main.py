import sys
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.exception.exception import CustomException
from src.logging.logger import logging
from src.entity.config_entity import DataIngestionConfig
from src.entity.config_entity import DataValidationConfig
from src.entity.config_entity import DataTransformationConfig
from src.entity.config_entity import TrainingPipelineConfig

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Initiate the data ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        logging.info("Initiate the data validation")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact ,data_validation_config)
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact ,data_transformation_config)
        logging.info("Initiate the data transformation")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        print(data_transformation_artifact)
    except Exception as e:
        raise CustomException(e,sys)


