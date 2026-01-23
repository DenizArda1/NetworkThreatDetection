import os
import sys
import numpy as np
import pandas as pd

# Data Ingestion related constants
DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME: str = "NetworkSecurityProjectDatabase"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "raw"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.8

# Data Validation related constants
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

# Data Transformation related constans
DATA_TRANSFORMATION_DIR_NAME: str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJ_DIR: str = "transformed_obj"
DATA_TRANSFORMATION_PREPROCESSING_OBJ_FILE_NAME: str = "preprocessing.pkl"

# Model Trainer related constants
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_FILE_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_OVERFIT_UNDERFIT_THRESHOLD: float = 0.05

# KNN imputer
DATA_TRANSFORMATION_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
}

HYPERPARAMETER_TUNING = {
            "Decision Tree": {
                'criterion': ['gini', 'entropy','log_loss'],
                'splitter': ['best', 'random'],
                'max_features': ['auto', 'sqrt', 'log2'],
            },
            "Random Forest": {
                'criterion': ['gini', 'entropy','log_loss'],
                'max_features': ['auto', 'sqrt', 'log2'],
                'n_estimators': [8,16,32,64],
            },
            "Gradient Boosting": {
                'loss': ['exponential','log_loss'],
                'learning_rate': [.1,.01,.05,.001],
                'subsample': [0.6,0.7,0.75,0.8,0.9],
                'criterion': ['squared_error','friedman_mse'],
                'max_features': ['auto', 'sqrt', 'log2'],
                'n_estimators': [8,16,32,64],
            },
            "Logistic Regression": {
                'penalty': ['l1', 'l2','elasticnet'],
                'C': [1,1.5,2,3,4],
                'l1_ratio': [.1,.2,.3,.4,.5]
            },
            "AdaBoost": {
                'n_estimators': [8,16,32,64],
                'learning_rate': [.1,.01,.05,.001],
            },
            "KNN": {
                'n_neighbors': [3,4,5,6],
                'weights': ['uniform','distance'],
                'algorithm': ['auto','ball_tree','kd_tree','brute'],
                'metric': ['minkowski', 'euclidean']
            }
        }

# Common constant variables
TARGET_COLUMN: str = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "artifacts"
FILE_NAME: str = "phisingData.csv"
SCHEMA_FILE_PATH: str = os.path.join("data_schema","schema.yaml")
SAVED_MODEL_DIR: str = os.path.join("saved_models")

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"