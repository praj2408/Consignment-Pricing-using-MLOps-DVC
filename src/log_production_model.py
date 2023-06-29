from stage1_Get_Data import GetData
import mlflow
import argparse
from mlflow.tracking import MlflowClient
from pprint import pprint
import joblib
import os 

class Log_Production_Model:
    def __init__(self):
        self.config="D:/Projects/Consignment/params.yaml"
        self.get_data=GetData().read_params(self.config)
        
    def log_production_model(self):
        self.config=self.get_data
        self.mlflow_config=self.config["mlflow_config_dir"]
        self.model_name=self.mlflow_config["registered_model_name"]
        self.remote_server_uri=self.mlflow_config["remote_server_uri"]
        mlflow.set_registry_uri(self.remote_server_uri)
        self.runs=mlflow.search_runs(experiment_ids=1)
        self.lowest_mae=self.runs["metrics.mae"].sort_values(ascending=True)[0]
        self.lowest_run_id=self.runs["run_id"][self.runs["metrics.mae"]==self.lowest_mae].values[0]
        self.clients=MlflowClient()
        for mv in self.clients.search_model_versions(f"name='{self.model_name}'"):
            mv = dict(mv)
        
        if mv["run_id"] == self.lowest_run_id:
            self.current_version = mv["version"]
            self.logged_model = mv["source"]
            pprint(mv, indent=4)
            self.clients.transition_model_version_stage(
                name=self.model_name,
                version=self.current_version,
                stage="Production"
            )
        else:
            self.current_version = mv["version"]
            self.client.transition_model_version_stage(
                name=self.model_name,
                version=self.current_version,
                stage="Staging"
            )        


        self.loaded_model = mlflow.pyfunc.load_model(self.logged_model)
        
        self.model_path = self.config["webapp_model_dir"] #"prediction_service/model"

        joblib.dump(self.loaded_model, self.model_path)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="params.yaml")
    parsed_args = args.parse_args()
    data = Log_Production_Model().log_production_model()