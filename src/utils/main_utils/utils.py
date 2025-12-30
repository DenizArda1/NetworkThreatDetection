import yaml
import os
import sys
import dill
import numpy as np
import pickle

from src.exception.exception import CustomException
from src.logging.logger import logging

def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e,sys)

def write_yaml_file(file_path:str, content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise CustomException(e,sys)

def save_numpy_arr_data(file_path:str, arr:np.ndarray):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_object:
            np.save(file_object, arr)
    except Exception as e:
        raise CustomException(e,sys)

def save_pkl_obj(file_path:str, obj:object)->None:
    try:
        logging.info("saving obj")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_object:
            pickle.dump(obj, file_object)
        logging.info("obj saved")
    except Exception as e:
        raise CustomException(e,sys)