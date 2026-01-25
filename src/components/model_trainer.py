import os
import sys
import mlflow

from src.exception.exception import CustomException
from src.logging.logger import logging
from src.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact
from src.entity.config_entity import ModelTrainerConfig
from src.constants.training_pipeline import HYPERPARAMETER_TUNING

from src.utils.main_utils.utils import save_obj,load_obj
from src.utils.main_utils.utils import load_numpy_arr_data
from src.utils.ml_utils.model.evaluate_model import evaluate_models
from src.utils.ml_utils.model.estimator import NetworkModel
from src.utils.ml_utils.metric.classification_metrics import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
   RandomForestClassifier,
   AdaBoostClassifier,
   GradientBoostingClassifier,
)
from sklearn.model_selection import GridSearchCV


import dagshub
dagshub.init(repo_owner='DenizArda1', repo_name='NetworkSecurity', mlflow=True)

class ModelTrainer:
    def __init__(self,model_trainer_config: ModelTrainerConfig,data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)

    def track_mlflow(self,best_model,classification_metric):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precision_score = classification_metric.precision_score
            recall_score = classification_metric.recall_score

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(
                sk_model=best_model,
                name="model"
            )

    def train_model(self,X_train,y_train,X_test,y_test):
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Logistic Regression": LogisticRegression(verbose=1),
            "KNN": KNeighborsClassifier(),
            "AdaBoost": AdaBoostClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
        }
        params = HYPERPARAMETER_TUNING
        model_report: dict = evaluate_models(X_train,y_train,
                                       X_test,y_test,models,params)
        best_model_name = max(model_report,key=model_report.get)
        best_model_score = model_report[best_model_name]
        best_model = models[best_model_name]
        model_param = params.get(best_model_name,{})

        if model_param:
            gs = GridSearchCV(best_model,model_param,cv=3)
            gs.fit(X_train,y_train)
            best_model = gs.best_estimator_
        else:
            best_model.fit(X_train,y_train)

        y_train_pred = best_model.predict(X_train)
        classification_train_metric = get_classification_score(y_true=y_train,y_pred=y_train_pred)

        # Tracking the mlflow
        self.track_mlflow(best_model,classification_train_metric)

        y_test_pred = best_model.predict(X_test)
        classification_test_metric = get_classification_score(y_true=y_test,y_pred=y_test_pred)

        self.track_mlflow(best_model,classification_test_metric)

        preprocessor = load_obj(self.data_transformation_artifact.transformed_obj_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_filepath)
        os.makedirs(model_dir_path, exist_ok=True)
        os.makedirs("final_model",exist_ok=True)

        logging.info("Saving model")
        network_model = NetworkModel(preprocessor=preprocessor,model=best_model)
        save_obj(self.model_trainer_config.trained_model_filepath,obj=network_model)

        save_obj("final_model/model.pkl",obj=best_model)

        model_trainer_artifact = ModelTrainerArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_filepath,
            train_metric_artifact=classification_train_metric,
            test_metric_artifact=classification_test_metric
        )
        return model_trainer_artifact


    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_arr_data(train_file_path)
            test_arr = load_numpy_arr_data(test_file_path)

            X_train, y_train, X_test, y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model_trainer_artifact = self.train_model(X_train,y_train,X_test,y_test)
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)
