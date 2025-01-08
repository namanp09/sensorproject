import sys
import os
import pandas as pd
import pickle
import yaml
from typing import Dict, Any
import boto3



from src.constant import *
from src.exception import CustomException
from src.logger import logging




class Mainutils:
    def __init__(self) -> None:
        pass

    def read_yaml_file(self, filename: str) -> dict:
        """
        Reads a YAML file and returns its contents as a dictionary.
        """
        try:
            with open(filename, "r") as yaml_file:  # Corrected mode to 'r'
                return yaml.safe_load(yaml_file)
        except Exception as e:
            raise CustomException(e, sys) from e

    def read_schema_config_file(self) -> dict:
        """
        Reads the schema configuration YAML file from the 'config' directory.
        """
        try:
            schema_config = self.read_yaml_file(os.path.join("config", "schema.yaml"))
            return schema_config
        except Exception as e:
            raise CustomException(e, sys) from e

    @staticmethod
    def save_objects(file_path: str, obj: object) -> None:
        """
        Saves a Python object to a file using pickle.
        """
        logging.info("Entered the save_objects method of Mainutils class")
        try:
            with open(file_path, "wb") as file_obj:
                pickle.dump(obj, file_obj)
                logging.info("Exited the save_objects method of Mainutils class")
        except Exception as e:
            raise CustomException(e, sys) from e

    @staticmethod
    def load_object(file_path: str) -> object:
        """
        Loads a Python object from a file using pickle.
        """
        logging.info("Entered the load_object method of Mainutils class")
        try:
            with open(file_path, "rb") as file_obj:
                obj = pickle.load(file_obj)
                logging.info("Exited the load_object method of Mainutils class")
                return obj
        except Exception as e:
            logging.info("Exception occurred in load_object method of Mainutils class")
            raise CustomException(e, sys) from e


    @staticmethod
    def load_object_alt(file_path: str) -> object:
        """
        Loads a Python object from a file using pickle (Alternative).
        """
        logging.info("Entered the load_object_alt method of Mainutils class")
        try:
            with open(file_path, "rb") as file_obj:
                return pickle.load(file_obj)
        except Exception as e:
            logging.info("Exception occurred in load_object_alt method of Mainutils class")
            raise CustomException(e, sys) from e
