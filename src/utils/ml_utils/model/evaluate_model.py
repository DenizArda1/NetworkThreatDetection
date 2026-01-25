import sys
from src.exception.exception import CustomException
from sklearn.metrics import f1_score
from sklearn.model_selection import GridSearchCV

def evaluate_models(X_train,y_train,X_test,y_test,models,params):
    try:
        report = {}
        for model_name,model_instance in models.items():
            model_params = params.get(model_name,{})

            gs = GridSearchCV(estimator=model_instance,param_grid=model_params,cv=3)
            gs.fit(X_train,y_train)

            best_model = gs.best_estimator_

            y_test_pred = best_model.predict(X_test)
            test_model_score = f1_score(y_test,y_test_pred)
            report[model_name] = test_model_score
        return report
    except Exception as e:
        raise CustomException(e,sys)