import os
import sys
from celery import Celery
from src.pipeline.training_pipeline import TrainingPipeline
from src.exception.exception import CustomException

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery_app = Celery(
    "network_security_worker",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

@celery_app.task(bind=True, name="train_model_task")
def train_model_task(self):
    try:
        training_pipeline = TrainingPipeline()
        training_pipeline.run_training_pipeline()
        return {"status": "Training Completed", "message": "Model trained successfully"}
    except Exception as e:
        raise CustomException(e, sys)