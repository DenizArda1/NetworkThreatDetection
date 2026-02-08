import sys
import os
import pandas as pd
import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")

import pymongo
from src.exception.exception import CustomException
from src.logging.logger import logging
from src.pipeline.training_pipeline import TrainingPipeline
from src.utils.main_utils.utils import load_obj
from src.utils.ml_utils.model.estimator import NetworkModel
from src.utils.main_utils.app_utils import train_model_task
from celery.result import AsyncResult

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from fastapi.responses import Response

from src.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME
from src.constants.training_pipeline import DATA_INGESTION_COLLECTION_NAME

from contextlib import asynccontextmanager

client = pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = client[DATA_INGESTION_COLLECTION_NAME]

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logging.info("Loading models into memory...")
        ml_models['preprocessor'] = load_obj("final_model/preprocessor.pkl")
        ml_models['model'] = load_obj("final_model/model.pkl")
        logging.info("Models loaded successfully.")
    except Exception as e:
        print(f"Error: {e}")
    yield
    ml_models.clear()
    logging.info("Models cleared from memory.")
app = FastAPI(lifespan=lifespan)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")


@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/train")
async def train():
    try:
        task = train_model_task.delay()
        return {
            "message": "Training task started successfully",
            "task_id": task.id
        }
    except CustomException as e:
        raise CustomException(e,sys)

@app.get("/task/{task_id}")
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=train_model_task.app)
    result = {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result
    }
    return result

@app.post("/predict")
async def predict(request: Request,file: UploadFile = File(...)):
    try:
        # Check if models are loaded
        if "preprocessor" not in ml_models or "model" not in ml_models:
            return Response("Error: Models are not loaded.", status_code=503)
        df = pd.read_csv(file.file)
        if 'Result' in df.columns:
            df = df.drop(columns=['Result'],axis=1)

        network_model = NetworkModel(preprocessor=ml_models['preprocessor'],model=ml_models['model'])
        y_pred = network_model.predict(df)
        df['Predicted'] = y_pred
        table_html = df.to_html(classes="table table-striped")
        return templates.TemplateResponse("table.html",{"request":request,"table":table_html})
    except CustomException as e:
        raise CustomException(e,sys)
    except Exception as e:
        print(e)
        return Response(f"Error: {e}")

if __name__ == "__main__":
    app_run(app,host="localhost",port=8000)