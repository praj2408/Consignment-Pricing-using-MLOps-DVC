# This python file is for fetching the data and dump to the folder called data
# import modules and libraries


import sys
import pandas as pd
import argparse
from app_exception.app_exception import AppException
from application_logging import logging
import yaml

class GetData:
    '''
    The main functionality is to get data from source 
    Function return None 
    '''

    def __init__(self):
        pass

    def read_params(self, config_path):
        try:
            logging.info("Reading all params from config_path")
            with open(config_path) as f:
                self.config = yaml.safe_load(f)
                logging.info("parameters readed from config_path successfully!!!")

                return self.config

        except Exception as e:
            logging.info(f"Exception Occurred while reading parameters from config_path -->{e}")
            raise AppException(e,sys)


    def get_data(self, config_path):
        try:
            logging.info("getting the data from the source")
            self.config = self.read_params(config_path)
            
            self.data_path = self.config["data_source"]["s3_source"]
            self.data = pd.read_csv(self.data_path, sep=',', encoding='utf-8')
        
            logging.info(f"Data Fetched from the source Successfully !!!")
            return self.data


        except Exception as e:
            logging.info(
                f"Exception Occurred while getting data from the source -->{e}")
            raise AppException(e, sys) from e





if __name__ == "__main__":
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()
    data = GetData().get_data(config_path=parsed_args.config)