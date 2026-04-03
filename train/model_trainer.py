import joblib
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from lightgbm import LGBMRegressor
from sklearn.metrics import root_mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV

from app.core.paths import  MODEL_PATH, PROCESSED_DATA_PATH
from app.utils.logger import logger
from app.utils.custom_exception import CustomException
from train.model_config import RANDOM_SEARCH_PARAMS, LIGHTGBM_PARAMS


class ModelTrainer:

    def __init__(self, artifacts_path : str ,model_path : str):
       
        self.artifacts_path = artifacts_path
        self.model_path = model_path
        self.random_search_params = RANDOM_SEARCH_PARAMS
        self.lightgbm_params = LIGHTGBM_PARAMS
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.lgnb_pipeline = None


    def load_data(self):
        try:
            logger.info("Loading splitted data.......")

            self.X_train = joblib.load(f"{self.artifacts_path}/X_train.joblib")
            self.X_test = joblib.load(f"{self.artifacts_path}/X_test.joblib")
            self.y_train = joblib.load(f"{self.artifacts_path}/y_train.joblib")
            self.y_test = joblib.load(f"{self.artifacts_path}/y_test.joblib")

            logger.info("Splitted data loaded successfully.")

        except Exception as e:
            logger.error(f"Error while loading splitted data : {e}")
            raise CustomException(f"Failed to load splitted data :", e)
        
    
    def transform_data(self):
        try:
            logger.info("Transforming data....")

            num_cols = self.X_train.select_dtypes(include = 'number').columns.tolist()
            cat_cols = [col for col in self.X_train.columns if col not in num_cols]

            logger.info(f"Numeric Columns : {num_cols}")
            logger.info(f"Categorical Columns : {cat_cols}")

            num_pipe = Pipeline(steps = [
                ('imputer', SimpleImputer(strategy = 'median')),
                ('scaler', StandardScaler())
            ])

            cat_pipe = Pipeline(steps = [
                ('imputer', SimpleImputer(strategy = 'constant', fill_value = 'missing')),
                ('encoder', OneHotEncoder(handle_unknown = 'ignore', sparse_output = False))
            ])

            preprocessor = ColumnTransformer(transformers = [
                ('num', num_pipe, num_cols),
                ('cat', cat_pipe, cat_cols)
            ])

            logger.info("Data transformation completed successfully.")

            return preprocessor
        
        except Exception as e:
            logger.error(f"Error while transforming data : {e}")
            raise CustomException("Failed to transform data :", e)

    
    def train_model(self, preprocessor):
        try:

            logger.info("Strating model training")

            lgbm_model =  LGBMRegressor(random_state = self.random_search_params["random_state"])

            lgbm_pipeline = Pipeline(steps=[
                ('pre', preprocessor),
                ('reg', lgbm_model)
            ])

            LGBM_PIPELINE_PARAMS = {f'reg__{k}': v for k, v in self.lightgbm_params.items()}

            random_search = RandomizedSearchCV(
                estimator = lgbm_pipeline, 
                param_distributions = LGBM_PIPELINE_PARAMS,
                n_iter = self.random_search_params["n_iter"],
                cv = self.random_search_params["cv"],
                n_jobs = self.random_search_params["n_jobs"],
                verbose = self.random_search_params["verbose"],
                random_state = self.random_search_params["random_state"],
                scoring = self.random_search_params["scoring"]
            )

            random_search.fit(self.X_train, self.y_train)

            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_
            best_score = abs(random_search.best_score_)

            logger.info("-" * 30)
            logger.info("HYPERPARAMETER TUNING RESULTS")
            logger.info("-" * 30)
            logger.info(f"Best CV RMSE: {best_score:,.3f}")
            logger.info("\nBest Parameters Found:")

            for param, value in best_params.items():
                
                clean_param = param.replace('reg__', '')
                logger.info(f"  - {clean_param}: {value}")

            logger.info("-" * 30)

            return best_lgbm_model

        except Exception as e:
            logger.error(f"Error while training_model : {e}")
            raise CustomException("Failed to train model :", e)
        

        
    def evaluate_and_save_model(self, model):
        try:

            logger.info("Evaluating model....")

            y_pred = model.predict(self.X_test)

            final_test_rmse = root_mean_squared_error(self.y_test, y_pred)

            y_train_pred = model.predict(self.X_train)

            r2score = r2_score(self.y_test, y_pred)

            final_train_rmse = root_mean_squared_error(self.y_train, y_train_pred)

            logger.info(f"Final Train RMSE: {final_train_rmse:,.3f}")
            logger.info(f"Final Test RMSE: {final_test_rmse:,.3f}")
            logger.info(f"R2 Score : {r2score}")
            logger.info(f"Generalization Gap: {final_test_rmse - final_train_rmse:,.3f}")


            logger.info("Saving Model....")

            joblib.dump(model, self.model_path)

            logger.info("Model saved successfully.")


        except Exception as e:
            logger.error("Error while evaluating and saving model : {e}")
            raise CustomException("Failed to evaluate and save model :", e)
        
    
    def run(self):
        try:
            logger.info("Starting model training pipeline.")

            self.load_data()

            preprocessor = self.transform_data()

            model = self.train_model(preprocessor)

            self.evaluate_and_save_model(model)

        except Exception as e:
            logger.error(f"Error while runnign model training pipeline : {e}")
            raise CustomException("Failed to run model training pipeline", e)
        
    

if __name__ == "__main__":

    trainer = ModelTrainer(PROCESSED_DATA_PATH, MODEL_PATH)
    trainer.run()