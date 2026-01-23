import sys
import os

from src.exception.exception import CustomException
from src.logging.logger import logging
from src.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_TRAINER_TRAINED_MODEL_FILE_NAME

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise CustomException(e,sys)
    def predict(self,x):
        try:
            x_transformed = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transformed)
            return y_hat
        except Exception as e:
            raise CustomException(e,sys)