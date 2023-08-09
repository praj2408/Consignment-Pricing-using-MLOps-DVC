import argparse
import numpy as np
from stage1_Get_Data import GetData
from stage3_preprocessing import Preprocessing
from stage2_Load_Data import LoadData
from sklearn.preprocessing import LabelEncoder
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import sys
from app_exception.app_exception import AppException
from application_logging import logging



class FeatureEngineering:
    '''
    This is the stage 4 of this machine learning pipeline this is for feature engineering technique 
    like outlier handling,column transformation using one hot and label encoding 
    function return and save data as 'tranformed_data' folder mentioned in params.yaml file
    '''

    def __init__(self):
        self.get_data = GetData()
        self.load_data = LoadData()
        
    def data_(self, config_path):
        try:
            logging.info("'data_' FUNCTION STARTED")
            self.config = self.get_data.read_params(config_path)
            self.data = self.config["data"]["processed"]
            self.data = pd.read_csv(self.data)
            logging.info("Data loaded successfully")
            return self.data
        except Exception as e:
            logging.info(
                 "Exception occurred while loading the data" + str(e))
            logging.info(
                 "Failed to load the data please check your code and run")
            raise AppException(e, sys) from e
    
    
    # outlier detection
    def outlier_detection(self, data, colname):
        self.data = data[data[colname] <= (
            data[colname].mean()+3*data[colname].std())]
        return self.data
    
    
    def remove_outliers(self, config_path):
        try:
            logging.info( "'remove_outliers' FUNCTION STARTED")
            self.data = self.data_(config_path)
            self.data0 = self.outlier_detection(self.data, "line_item_value")
            self.data1 = self.outlier_detection(
                self.data0, "unit_of_measure_(per_pack)")
            self.data2 = self.outlier_detection(self.data1, "pack_price")
            self.data3 = self.outlier_detection(self.data2, "unit_price")
            # self.data4=self.outlier_detection(self.data3,"days_to_process")
            self.data = self.data3
            logging.info(
                 "removed outliers function compiled successfully")
            return self.data
        except Exception as e:
            logging.info(
                 "Exception occured in remove_outliers method"+str(e))
            logging.info( "Error occured while removing outliers")
            raise AppException(e, sys) from e



    def trans_freight_cost(self, x):
            if x.find("See") != -1:
                return np.nan
            elif x == "Freight Included in Commodity Cost" or x == "Invoiced Separately":
                return 0
            else:
                return x

    def freight_cost_transform(self, config_path):
        try:
            logging.info(
                 "'freight_cost_transform' FUNCTION STARTED")
            self.data = self.remove_outliers(config_path)
            self.data["freight_cost_(usd)"] = self.data["freight_cost_(usd)"].apply(
                self.trans_freight_cost)
            self.median_value = self.data["freight_cost_(usd)"].median()
            self.data["freight_cost_(usd)"] = self.data["freight_cost_(usd)"].replace(
                np.nan, self.median_value)
            self.data["freight_cost_(usd)"] = self.data["freight_cost_(usd)"].astype(
                float)
            logging.info("freight_cost_transform function compiled successfully")
     
            return self.data
        except Exception as e:
            logging.info(
                 "Exception occurred while compiling the code" + str(e))
            logging.info(
                 "Failed to execute the code please check your code and run")
            raise AppException(e, sys) from e


    def feature_engineering(self, config_path):
        try:
            logging.info( "'feature_engineering' FUNCTION STARTED")
            lb=LabelEncoder()
            self.data = self.freight_cost_transform(config_path)
            self.data.drop("pq_#",axis=1,inplace=True)
            self.data["po_/_so_#"]=pd.get_dummies(self.data["po_/_so_#"],drop_first=True,dtype=int)
            self.data["asn/dn_#"]=pd.get_dummies(self.data["asn/dn_#"],drop_first=True,dtype=int)
            
            self.data["country"]=lb.fit_transform(self.data["country"])
            self.data["fulfill_via"]=pd.get_dummies(self.data["fulfill_via"],drop_first=True,dtype=int)
            self.data["vendor_inco_term"]=lb.fit_transform(self.data["vendor_inco_term"])
            self.data["sub_classification"]=lb.fit_transform(self.data["sub_classification"])

            self.data["first_line_designation"]=pd.get_dummies(self.data["first_line_designation"],drop_first=True,dtype=int)

            self.data["shipment_mode"] = lb.fit_transform(self.data["shipment_mode"])            
            logging.info(
                 "feature engineering function compiled successfully")
            return self.data
            # [data for data in self.data if self.data[data].dtypes=="O"]
        except Exception as e:
            logging.info(
                 "Exception occurred while compiling the code" + str(e))
            logging.info(
                 "Failed to execute the code please check your code and run")
            raise AppException(e, sys) from e

    def final_data(self,config_path):
        try:
            
            logging.info( "'data' FUNCTION STARTED")
            self.finaldata = self.feature_engineering(config_path)
            self.config = self.get_data.read_params(config_path)
            self.data.drop("Unnamed: 0", axis=1, inplace=True)
            self.data.to_csv(self.config["final_data"]["transformed_data"], index=False)
            logging.info( "Final Data for prediction successfully created")
        except Exception as e:
            logging.info(
                 "Exception occurred while compiling the code" + str(e))
            logging.info(
                 "Failed to execute the code please check your code and run")
            raise AppException(e, sys) from e


if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument(
        "--config", default="params.yaml")
    parsed_args = args.parse_args()
    data = FeatureEngineering().final_data(config_path=parsed_args.config)
    #print(FeatureEngineering().feature_engineering("/home/dataguy/Desktop/Consignment-Pricing-Using-Mlops-DVC-main/params.yaml"))