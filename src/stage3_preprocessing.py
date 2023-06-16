from stage1_Get_Data import GetData
from stage2_Load_Data import LoadData
import pandas as pd
import numpy as np
import argparse
import sys
from app_exception.app_exception import AppException
from application_logging import logging


def column_imputation(config_path):
        try:
            logging.info("'column_imputation' FUNCTION STARTED")
            self.data = self.get_data.get_data(config_path)
            self.data.columns = self.data.columns.str.lower()
            self.data.columns = self.data.columns.str.replace(" ", "_")
            logging.info("'column_imputation' FUNCTION COMPILED SUCCESSFULLY")
            return self.data
        except Exception as e:
            logging.info(
                f"Exception occurred while compiling the code {str(e)}")
            logging.info(
                "Failed to execute the code please check your code and run")
            raise AppException(e, sys) from e