import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from app.core.paths import PROCESSED_DATA_PATH, DATASET_PATH
from app.utils.logger import logger
from app.utils.custom_exception import CustomException


class DataPreprocessor:

    def __init__(self, data_path : str, artifacts_path : str):
        
        self.data_path = data_path
        self.artifacts_path = artifacts_path
        self.df : pd.DataFrame = None

        if not os.path.exists(self.artifacts_path):
            os.makedirs(self.artifacts_path)


    def load_data(self):
        try: 
            logger.info("Loading Dataset.....")
            self.df = pd.read_csv(self.data_path)
            logger.info("Dataset loaded successfully.")

        except Exception as e:
            logger.error(f"Error while loading dataset : {e}")
            raise CustomException("Failed to load dataset : ", e)
        
    
    def clean_data(self):
        try:
            logger.info("Cleaning dataset...")

            self.df = self.df.drop(columns = ['model', "name", "edition"])
            self.df = self.df.drop_duplicates()

            logger.info(f"Dataset cleaned successfully.")

        except Exception as e:
            logger.error(f"Error while cleaning dataset : {e}")
            raise CustomException(f"Failed to clean dataset : ", e)
        
    
    def split_and_save_data(self):
        try:
            logger.info("Splitting data....")

            X = self.df.drop(columns = 'selling_price')
            y = self.df.selling_price.copy()

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 42)

            logger.info(f"X train shape : {X_train.shape}, Y train shape :  {y_train.shape}")
            logger.info(f"X test shape : {X_test.shape}, Y test shape :  {y_test.shape}")

            logger.info("Data splitted successfully.")

            logger.info("Saving splitted data....")

            joblib.dump(X_train, f"{self.artifacts_path}/X_train.pkl")
            joblib.dump(X_test, f"{self.artifacts_path}/X_test.pkl")
            joblib.dump(y_train, f"{self.artifacts_path}/y_train.pkl")
            joblib.dump(y_test, f"{self.artifacts_path}/y_test.pkl")

            logger.info("Splitted data saved successfully.")

        except Exception as e:
            logger.error(f"Error while splitting and saving data : {e}")
            raise CustomException(f"Failed to split and save data : ", e)
        

    def process(self):
        try:
            self.load_data()
            self.clean_data()
            self.split_and_save_data()

        except Exception as e:
            logger.error(f"Error while running data processing pipelien : {e}")
            raise CustomException("Failed to run data processing pipeline : ", e)


if __name__ == "__main__":

    processor = DataPreprocessor(DATASET_PATH, PROCESSED_DATA_PATH)
    processor.process()