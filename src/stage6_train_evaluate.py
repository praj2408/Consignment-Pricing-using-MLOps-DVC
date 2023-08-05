from distutils.command.config import config
from urllib.parse import urlparse
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from stage1_Get_Data import GetData
import os
import json
import joblib
from application_logging import logging
from app_exception.app_exception import AppException
import argparse
from sklearn.model_selection import RandomizedSearchCV
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import sys
import mlflow
from datetime import datetime

MODEL_DIR = "saved_models"
MODEL_PATH = os.path.join(os.getcwd(), MODEL_DIR)
print(MODEL_PATH)
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y_%m_%d_%H_%M')}"
folder_name=CURRENT_TIME_STAMP
MAIN_PATH=os.path.join(MODEL_PATH,folder_name)

class TrainEvaluate:
    def __init__(self):
        self.get_data = GetData()
        self.filename="model_rf.pkl"

    def evaluation_metrics(self, act, pred):
        self.r2_score = r2_score(act, pred)
        self.mse = mean_squared_error(act, pred)
        self.rmse = np.sqrt(mean_squared_error(act, pred))
        return self.r2_score, self.mse, self.rmse

    def model_eval(self, config_path):
        try:
            logging.info("'train_evaluate' function started")
            self.config = self.get_data.read_params(config_path)
            self.test_data = self.config["split_data"]["test_path"]
            self.train_data = self.config["split_data"]["train_path"]
            self.model_dir = self.config["model_dirs"]
            self.target_col = self.config["base"]["target_data"]
            
            logging.info("train data read successfully-->path: "+self.train_data)
            self.train = pd.read_csv(self.train_data, sep=",")
            logging.info("train data read successfully")
            self.test = pd.read_csv(self.test_data, sep=",")
            logging.info("test data read successfully")
            
            
            logging.info("model training started")
            self.criterion = self.config["estimators"]["RandomForestRegressor"]["params"]["criterion"]
            self.max_deapth = self.config["estimators"]["RandomForestRegressor"]["params"]["max_deapth"]
            self.min_sample_leaf = self.config["estimators"]["RandomForestRegressor"]["params"]["min_sample_leaf"]
            self.n_estimators = self.config["estimators"]["RandomForestRegressor"]["params"]["n_estimators"]
            self.min_sample_split = self.config["estimators"]["RandomForestRegressor"]["params"]["min_sample_split"]
            self.oob_score = self.config["estimators"]["RandomForestRegressor"]["params"]["oob_score"]
            self.x_train, self.x_test = self.train.drop(
                self.target_col, axis=1), self.test.drop(self.target_col, axis=1)
            self.y_train, self.y_test = self.train[self.target_col], self.test[self.target_col]



            rf = RandomForestRegressor()
            
            rf.fit(self.x_train, self.y_train)
            
            RCV = RandomizedSearchCV(estimator=rf,
                                        param_distributions=self.config["RandomizedSearchCV"]["params"],
                                        n_iter=self.config["RandomizedSearchCV"]["n_iter"],
                                        scoring=self.config["RandomizedSearchCV"]["scoring"],
                                        cv=self.config["RandomizedSearchCV"]["cv"],
                                        verbose=self.config["RandomizedSearchCV"]["verbose"],
                                        random_state=42,
                                        n_jobs=self.config["RandomizedSearchCV"]["n_jobs"],
                                        return_train_score=self.config["RandomizedSearchCV"]["return_train_score"])
            rf1 = RCV.fit(self.x_train, self.y_train)
            
            print(RCV.best_score_)
            
            
                # Feature importances
            # self.rf_feature_imp = pd.DataFrame(
            #     rf.feature_importances_, index=self.x_train.columns, columns=['Feature_importance'])

            # self.rf_feature_imp.sort_values(
            #     by='Feature_importance', ascending=False, inplace=True)

            # print(round(self.rf_feature_imp, 3))
                
            # self.rf1_feature_imp['Feature_importance'] = self.rf1_feature_imp[self.rf1_feature_imp['Feature_importance'] > 0.001]

            # self.rf1_feature_imp = self.rf1_feature_imp[self.rf1_feature_imp['Feature_importance'].notna()]
            # self.features_by_rf = self.rf1_feature_imp.index

            y_pred = rf1.predict(self.x_test)
            logging.info("Model Trained on RandomizedSearchCV successfully")
            
            (r2, mse, rmse) = self.evaluation_metrics(self.y_test, y_pred)
            print(r2*100, mse, rmse)

            # normalized_rmse=rmse/(63770.43-1121)
            # print(f"normalized rmse::{normalized_rmse}")

            os.makedirs(self.model_dir, exist_ok=True)
            os.makedirs(MAIN_PATH,exist_ok=True)
            self.model_path = os.path.join(MAIN_PATH,self.filename)
            joblib.dump(rf1, self.model_path)

            scores_file = self.config["reports"]["scores"]
            params_file = self.config["reports"]["params"]

            with open(scores_file, "w") as f:
                scores = {
                    "rmse": rmse,
                    "r2 score": r2*100,
                    "mse": mse,
                    "train_score": rf.score(self.x_train, self.y_train),
                    "test_score": rf.score(self.x_test, self.y_test)
                }
                json.dump(scores, f, indent=4)
            logging.info("scores written to file")
            
            with open(params_file, "w") as f:
                params = {
                    "best params": RCV.best_params_,
                    "criterion": self.criterion,
                    "n_estimators": self.n_estimators,
                    "max_deapth": self.max_deapth,
                    "min_sample_leaf": self.min_sample_leaf,
                    "min_sample_split": self.min_sample_split,
                    "oob_score": self.oob_score
                }
                json.dump(params, f, indent=4)

        except Exception as e:
            logging.info("Exception occured in 'train_evaluate' function"+str(e))
            logging.info("train_evaluate function reported error in the function")
            raise AppException(e, sys) from e


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument(
        "--config", default="params.yaml")
    parsed_args = args.parse_args()
    data = TrainEvaluate().model_eval(config_path=parsed_args.config)