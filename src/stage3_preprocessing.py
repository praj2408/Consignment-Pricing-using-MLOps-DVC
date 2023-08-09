from stage1_Get_Data import GetData
from stage2_Load_Data import LoadData
import pandas as pd
import numpy as np
import argparse
import sys
from app_exception.app_exception import AppException
from application_logging import logging


class Preprocessing:
    '''
    This class is for preprocessing the data like column_imputation,missing_value_handling,transforming the
    columns and so on
    class return and save csv data to the specified folder path mentioned in params.yaml file
    '''
    def __init__(self):
        self.load_data = LoadData()
        self.get_data = GetData()

    def column_imputation(self, config_path):
        try:
            logging.info("'column_imputation' FUNCTION STARTED")
            self.data = self.get_data.get_data(config_path)
            self.data.columns = self.data.columns.str.lower()
            self.data.columns = self.data.columns.str.replace(" ", "_")
            #self.data.columns = self.data.columns.str.replace("#", "")
            logging.info("'column_imputation' FUNCTION COMPILED SUCCESSFULLY")
            return self.data
        
        except Exception as e:
            logging.info(
                f"Exception occurred while compiling the code {str(e)}")
            logging.info(
                "Failed to execute the code please check your code and run")
            raise AppException(e, sys) from e

    def impute_missing(self, config_path):
        try:
            logging.info("'impute_missing' FUNCTION STARTED")
            self.data = self.column_imputation(config_path)
            self.data = self.data.drop("dosage", axis=1)
            self.data["shipment_mode"].fillna("Air", inplace=True)
            self.data["line_item_insurance_(usd)"].fillna(47.04, inplace=True)
            logging.info("'impute_missing' FUNCTION COMPILED SUCCESSFULLY")
            return self.data
        except Exception as e:
            logging.info(
                f"Exception occurred while compiling the code {str(e)}")
            logging.info(
                "Failed to execute the code please check your code and run")
            raise AppException(e, sys) from e

    def client_dates(self, date):
        if date == "Pre-PQ Process":
            return pd.to_datetime('01/06/2009', format="%d/%m/%Y")
        elif date == "Date Not Captured":
            return "Date Not Captured"
        else:
            if len(date) < 9:
                date = pd.to_datetime(date, format="%m/%d/%y")
                return date
            else:
                date = date.replace("-", "/")
                date = pd.to_datetime(date, format="%d/%m/%Y")
                return date

    def transform_pq_first_sent_to_client_date_columns(self, config_path):
        try:
            logging.info(
                "'transform_pq_first_sent_to_client_date_columns' FUNCTION STARTED")
            self.data = self.impute_missing(config_path)
            self.data["pq_first_sent_to_client_date"] = self.data["pq_first_sent_to_client_date"].apply(
                self.client_dates)
            self.data = self.data.drop(
                self.data.index[self.data["pq_first_sent_to_client_date"] == "Date Not Captured"])
            logging.info(
                "'transform_pq_first_sent_to_client_date_columns' FUNCTION COMPILED SUCCESSFULLY")
            return self.data
        except Exception as e:
            logging.info("Exception occurred while compiling the code", str(e))
            logging.info(
                "Failed to execute the code please check your code and run")
            raise AppException(e, sys) from e

    def transform_dates(self, data):
        data = data.replace("-", "/")
        data = pd.to_datetime(data, format="%d/%b/%y")
        return data

    def transform_dates_columns(self, config_path):
        try:
            logging.info("'transform_dates_columns' FUNCTION STARTED")
            self.data = self.transform_pq_first_sent_to_client_date_columns(
                config_path)
            self.data["delivery_recorded_date"] = self.data["delivery_recorded_date"].apply(
                self.transform_dates)
            self.data["delivered_to_client_date"] = self.data["delivered_to_client_date"].apply(
                self.transform_dates)
            self.data["pq_first_sent_to_client_date"] = pd.to_datetime(self.data["pq_first_sent_to_client_date"])
            
            self.data["days_to_process"] = self.data["delivery_recorded_date"]-self.data["pq_first_sent_to_client_date"]
            self.data["days_to_process"] = pd.to_timedelta(self.data["days_to_process"])
            self.data['days_to_process'] = self.data['days_to_process'].dt.days.astype(
                'int64')
            logging.info(
                "transform_dates_columns function compiled successfully")
            return self.data
        except Exception as e:
            logging.info("Exception occurred while compiling the code", str(e))
            logging.info(
                "Failed to execute the code please check your code and run")
            raise AppException(e, sys) from e
        
    def reorder(self, data):
        data=data.split("-")
        data=data[0]
        return data   
     

    def trans_freight_cost(self, x):
        if x.find("See") != -1:
            return np.nan
        elif x == "Freight Included in Commodity Cost" or x == "Invoiced Separately":
            return 0
        else:
            return x

    def transform_freight_cost_columns(self, config_path):
        try:
            logging.info("'transform_freight_cost_columns' FUNCTION STARTED")
            self.data = self.transform_dates_columns(config_path)
            self.data = self.reorder_columns(config_path)
            self.data["freight_cost_(usd)"] = self.data["freight_cost_(usd)"].apply(
                self.trans_freight_cost)

            self.median_value = self.data["freight_cost_(usd)"].median()
            self.data["freight_cost_(usd)"] = self.data["freight_cost_(usd)"].replace(
                np.nan, self.median_value)
            logging.info(
                "transform_freight_cost_columns function compiled successfully")
            return self.data
        except Exception as e:
            raise AppException(e, sys) from e

    def drop_unnecessary_columns(self, config_path):
        try:
            logging.info("'drop_unnecessary_columns' FUNCTION STARTED")
            self.config = self.get_data.read_params(config_path)
            self.data = self.transform_dates_columns(config_path)
            self.data = self.data[self.config["columns"]["select"]]
            logging.info(
                "drop_unnecessary_columns function compiled successfully")
            return self.data
        except Exception as e:
            logging.info("Exception occurred while compiling the code", str(e))
            logging.info(
                "Failed to execute the code please check your code and run")
            raise AppException(e, sys) from e
        
        

        
        
        
        
        
        
        
        

    def data_(self, config_path):
        try:
            logging.info("'data' FUNCTION STARTED")
            self.config = self.get_data.read_params(config_path)
            self.data = self.drop_unnecessary_columns(config_path)
            
            self.data["po_/_so_#"] = self.data["po_/_so_#"].apply(self.reorder)
            self.data["asn/dn_#"] = self.data["asn/dn_#"].apply(self.reorder)
            
            
            self.data.to_csv(self.config["data1"]["processed"])
            logging.info("data function compiled successfully")
        except Exception as e:
            logging.info("Exception occurred while compiling the code")
            logging.info(
                "Failed to execute the code please check your code and run")
            raise AppException(e, sys) from e

if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument(
        "--config", default="params.yaml")
    parsed_args = args.parse_args()
    data = Preprocessing().data_(config_path=parsed_args.config)