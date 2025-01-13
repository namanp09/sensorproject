import sys
import os
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.constant import *
from src.exception import CustomException
from src.logger import logging
from src.utils.main_utils import MainUtils
from dataclasses import dataclass


@dataclass
class DataTransformationConfig:
    artifact_dir = os.path.join(artifact_folder)
    transformed_train_file_path = os.path.join(artifact_dir,'train.npy')
    transformed_test_file_path = os.path.join(artifact_dir,'test.npy')
    transformed_object_file_path = os.path.join(artifact_dir,'preprocessor.pkl')


class DataTransformation:
    def __init__(self,feature_store_file_path):
        self.feature_store_file_path = feature_store_file_path

        self.data_transformation_config = DataTransformationConfig()

        self.utils = MainUtils()

    @staticmethod
    def get_data(feature_store_file_path: str) ->pd.DataFrame:

        try:

            data = pd.read_csv(feature_store_file_path)

            data.rename(columns={"Good/Bad": TARGET_COLUMN}, inplace=True)

            return data
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_data_transformer_object(self, dataframe: pd.DataFrame):

        try:
        # Dynamically identify numeric and categorical columns
            numeric_columns = dataframe.select_dtypes(include=['number']).columns.tolist()
            categorical_columns = dataframe.select_dtypes(exclude=['number']).columns.tolist()

        # Define transformation steps for numeric and categorical data
            numeric_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
            ('scaler', RobustScaler())
            ])

            categorical_transformer = Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
            ])

        # Create ColumnTransformer
            preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numeric_columns),
                ('cat', categorical_transformer, categorical_columns)
            ]
            )

            return preprocessor
        
        except Exception as e:
            raise CustomException(e, sys)

    
    def initiate_data_transformation(self):

        logging.info("Entered initiate data transformation method of data transformation class")

        try:
        # Read data
            dataframe = self.get_data(feature_store_file_path=self.feature_store_file_path)

        # Split features and target
            X = dataframe.drop(columns=TARGET_COLUMN)
            y = np.where(dataframe[TARGET_COLUMN] == -1, 0, 1)

        # Split into training and testing data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        # Get preprocessor object
            preprocessor = self.get_data_transformer_object(dataframe=X)

        # Transform the data
            X_train_scaled = preprocessor.fit_transform(X_train)
            X_test_scaled = preprocessor.transform(X_test)

        # Save the preprocessor
            preprocessor_path = self.data_transformation_config.transformed_object_file_path
            os.makedirs(os.path.dirname(preprocessor_path), exist_ok=True)
            self.utils.save_object(file_path=preprocessor_path, obj=preprocessor)

        # Combine transformed features with target
            train_arr = np.c_[X_train_scaled, np.array(y_train)]
            test_arr = np.c_[X_test_scaled, np.array(y_test)]

            return (train_arr, test_arr, preprocessor_path)

        except Exception as e:
            raise CustomException(e, sys) from e


    