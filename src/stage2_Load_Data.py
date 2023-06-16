# read the data from data source
# save it in data/raw
import os
import sys
from stage1_Get_Data import read_params, get_data
import argparse
from application_logging import logging
from app_exception.app_exception import AppException


def load_and_save(config_path):
        
    try:
        logging.info(f"Loading data from the source")
        config = read_params(config_path)
        df = get_data(config_path)
        raw_data_path = config['load_data']['raw_dataset']
        df.to_csv(raw_data_path, sep=',', encoding='utf-8')
        logging.info(f"Data Loaded from the source Successfully !!!")
    
    except Exception as e:
        logging.info(
            f"Exception Occurred while loading data from the source -->{e}")
        raise AppException(e, sys) from e



if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args = args.parse_args()
    load_and_save(config_path=parsed_args.config)