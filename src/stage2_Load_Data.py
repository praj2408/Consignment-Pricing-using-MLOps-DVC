# read the data from data source
# save it in data/raw
import os
import sys
from stage1_Get_Data import GetData
import argparse
from application_logging import logging
from app_exception.app_exception import AppException


class LoadData:
    '''
    The main functionality of this class is to load the data to the folder path
    we have assigned in params.yaml file
    function return data and save it to folder we have assigned
    '''

    def __init__(self):
        self.getdata = GetData()

    def load_data(self, config_path):
            
        try:
            logging.info(f"Loading data from the source")
            self.config = self.getdata.read_params(config_path)
            self.data = self.getdata.get_data(config_path)
            self.raw_data_path = self.config['load_data']['raw_dataset']
            self.data.to_csv(self.raw_data_path, sep=',', encoding='utf-8', index=False)
            logging.info(f"Data Loaded from the source Successfully !!!")
        
        except Exception as e:
            logging.info(
                f"Exception Occurred while loading data from the source -->{e}")
            raise AppException(e, sys) from e



if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()
    LoadData().load_data(config_path=parsed_args.config)