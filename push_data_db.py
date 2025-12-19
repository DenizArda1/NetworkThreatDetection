import os
import sys
import pandas as pd
import pymongo
from pymongo import MongoClient

from src.exception.exception import CustomException
from src.logging.logger import logging
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

import certifi
ca_cert = certifi.where()

class NetworkDataExtractor:
    def __init__(self, database, collection):
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[database]
            self.collection = self.database[collection]
        except Exception as e:
            raise CustomException(e, sys)

    def csv_to_json(self, file_path):
        try:
            data = pd.read_csv(file_path)
            return data.to_dict(orient="records")
        except Exception as e:
            raise CustomException(e, sys)

    def insert_data_mongodb(self, records):
        try:
            if not records:
                return 0
            self.collection.insert_many(records)
            return len(records)
        except Exception as e:
            raise CustomException(e, sys)





