from typing import Any

import pandas as pd
from prophet import Prophet
from typing_extensions import Self

from ..analytics.evaluationMetrics import evaluations
from ..datapreparation.datapreparation_utils import PreprocessingTeleconsulto, logger
from ..datapreparation.prep import PreprocessingClass
from ..utility.experiment_utils import create_zero_dataframe
from ..utility.constants import predict_dataframe_columns
from .algorithm import Prophet_model, prophet_tuning
from .prophet_utils import (
    preprocess_prophet_input,
    preprocess_prophet_output,
    train_val_test_split,
)


def preprocess_and_split_df(
    preprocessor: PreprocessingClass,
    df: pd.DataFrame,
    time_granularity: str,
    val_size: float,
    test_size: float = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Preprocess the filtered DataFrame and split it into train, validation, and test sets.

    Parameters
    ----------
    preprocessor : PreprocessingClass
        An instance of the PreprocessingClass used for data preprocessing.
    df : pd.DataFrame
        The DataFrame to be preprocessed and split.
    val_size : float
        The percentage of validation data
    test_size : float, optional
        The percentage of test data. Default is None


    Returns
    -------
    tuple
        tuple: A tuple containing four DataFrames: (df_preproc, df_train, df_val, df_test).
    """
    full_df = preprocessor.fit_transform(df, time_granularity=time_granularity)
    full_df = preprocess_prophet_input(full_df, date="Timestamp", target="Target")
    df_train, df_val, df_test = train_val_test_split(full_df, val_size, test_size)
    return full_df, df_train, df_val, df_test


class ExperimentModel:
    def __init__(self, preprocessor: PreprocessingTeleconsulto):
        self.preprocessor = preprocessor
        self.models_dict: dict[str, Prophet_model] = {}

    def fit(
        self,
        df: pd.DataFrame,
        dict_id_pred_queries: dict[str, str],
        hyperparameters_grid: dict[str, Any],
        time_granularity: str,
        val_size: float,
        test_size: float = None,
        max_na_ratio: float = 0.5,
    ) -> Self:
        count = 0
        # Train and tune all models for all the possible levels in the hierarchy
        for id_pred, query in dict_id_pred_queries.items():
            self.models_dict[id_pred] = None
            logger.info(f"START training {id_pred}")
            filtered_df = df.query(query)
            full_df, df_train, df_val, df_test = preprocess_and_split_df(
                self.preprocessor, filtered_df, time_granularity, val_size, test_size
            )
            if full_df.isna().sum().sum() / len(full_df) >= max_na_ratio:
                logger.info(
                    f"The time series {id_pred} has more than {max_na_ratio*100}% null values, skipping it."
                )
                count += 1
                logger.info(
                    f"Remaining number of iteration - {len(dict_id_pred_queries.keys())-count}"
                )
                continue
            try:
                # Tune if we have a non-empty validation set
                best_params = prophet_tuning(hyperparameters_grid, df_train, df_val)
                Model = Prophet_model(best_params)
                # Retrain on train and val data with best parameters
                Model.fit(pd.concat([df_train, df_val]))
            except ValueError as e:
                logger.info(f"Skipping training {id_pred}, due to: {e}")
                count += 1
                logger.info(
                    f"Remaining number of iteration - {len(dict_id_pred_queries.keys())-count}"
                )
                continue

            self.models_dict[id_pred] = Model
            logger.info(f"DONE training {id_pred}")

            count += 1
            logger.info(
                f"Remaining number of iteration - {len(dict_id_pred_queries.keys())-count}"
            )

        return self

    def create_hyperparameters_table(
        self, hyperparameters: dict[str, Any]) -> dict[str, Any]:
        def get_params_to_log(
            model: Prophet, hyperparameters: list[str]) -> dict[str, Any]:
            return {hyper: getattr(model, hyper) for hyper in hyperparameters}

        return {id_pred.replace('/', '_') : get_params_to_log(model.model, list(hyperparameters.keys())) if model else None 
                for id_pred, model in self.models_dict.items()}

    def predict(
        self,
        df: pd.DataFrame,
        dict_id_pred_queries: dict[str, str],
        time_granularity: str,
        val_size: float,
        test_size: float = None,
        ) -> pd.DataFrame:
        predictions = []
        for id_pred, query in dict_id_pred_queries.items():
            logger.info(f"START predicting {id_pred}")
            filtered_df = df.query(query)
            full_df, df_train, df_val, df_test = preprocess_and_split_df(
                self.preprocessor, filtered_df, time_granularity, val_size, test_size
            )

            model = self.models_dict[id_pred]
            if model is None:
                logger.info(
                    f"Skipping prediction for {id_pred}, as the model has not been trained"
                )
                df_output = create_zero_dataframe(
                    predict_dataframe_columns,
                    len(df_test),
                )
                df_output['Id_pred'] = id_pred
                df_output['Timestamp'] = df_test['ds']
            else:
                try:
                    df_test_pred = model.model.predict(df_test)
                    df_output = preprocess_prophet_output(df_test_pred, id_pred)
                except ValueError as e:
                    logger.info(f"Skipping prediction for {id_pred}, due to: {e}")
                    df_output = create_zero_dataframe(
                        predict_dataframe_columns,
                        len(df_test),
                    )
                    df_output['Id_pred'] = id_pred
                    df_output['Timestamp'] = df_test['ds']
            # Evaluate model
            predictions.append(df_output)
            logger.info(f"DONE predicting {id_pred}")

        return pd.concat(predictions)

    def evaluate(
        self,
        df: pd.DataFrame,
        dict_id_pred_queries: dict[str, str],
        time_granularity: str,
        val_size: float,
        test_size: float = None,
    ) -> pd.DataFrame:
        
        metrics = []
        predictions = self.predict(df, dict_id_pred_queries, time_granularity, val_size, test_size)
        for id_pred, query in dict_id_pred_queries.items():
            logger.info(f"START predicting {id_pred}")
            filtered_df = df.query(query)
            full_df, df_train, df_val, df_test = preprocess_and_split_df(
                self.preprocessor, filtered_df, time_granularity, val_size, test_size
            )

            df_test = df_test.rename(columns={'ds':'Timestamp', 'y': 'Target'})
            df_pred = predictions[predictions["Id_pred"] == id_pred]
            metrics.append(evaluations(df_test, df_pred, date='Timestamp' , y_true='Target', y_pred='Pred_mean'))  

        metrics = pd.concat(metrics).dropna()
        return metrics


class ExperimentModel_sperimentale:
    def __init__(self, preprocessor: PreprocessingTeleconsulto, use_model : str):
        self.preprocessor = preprocessor
        self.use_model = use_model
        self.models_dict: dict[str, Prophet_model] = {}

    def fit(
        self,
        df: pd.DataFrame,
        dict_id_pred_queries: dict[str, str],
        hyperparameters_grid: dict[str, Any],
        time_granularity: str,
        val_size: float,
        test_size: float = None,
        max_na_ratio: float = 0.5,
    ) -> Self:
        count = 0
        # Train and tune all models for all the possible levels in the hierarchy
        for id_pred, query in dict_id_pred_queries.items():
            self.models_dict[id_pred] = None
            logger.info(f"START training {id_pred}")
            filtered_df = df.query(query)
            full_df, df_train, df_val, df_test = preprocess_and_split_df(
                self.preprocessor, filtered_df, time_granularity, val_size, test_size
            )
            if full_df.isna().sum().sum() / len(full_df) >= max_na_ratio:
                logger.info(
                    f"The time series {id_pred} has more than {max_na_ratio*100}% null values, skipping it."
                )
                count += 1
                logger.info(
                    f"Remaining number of iteration - {len(dict_id_pred_queries.keys())-count}"
                )
                continue
            try:

                ########################################################################
                # NON SPECIFIC MODEL SELECT # -> SPERIMENTALE
                # Tune if we have a non-empty validation set
                #
                # Function must be <model>_tuning(param_grid: dict, train_df: DataFrame, validation_df: DataFrame, 
                #                                 weight_rmse: float = 0.5, weight_mape: float = 0.5)
                best_params = eval(f'{self.use_model.lower()}_tuning(param_grid=hyperparameters_grid, train_df=df_train, validation_df=df_val)')
                #
                # Class must be <Model>_mode(dic_param: dict) and needs to have implemented 
                # fit(self, df: pd.DataFrame)
                # predict(self, df: pd.DataFrame)
                Model = eval(f'{self.use_model.title()}_model(best_params)')
                ########################################################################

                Model.fit(pd.concat([df_train, df_val]))
            except ValueError as e:
                logger.info(f"Skipping training {id_pred}, due to: {e}")
                count += 1
                logger.info(
                    f"Remaining number of iteration - {len(dict_id_pred_queries.keys())-count}"
                )
                continue

            self.models_dict[id_pred] = Model
            logger.info(f"DONE training {id_pred}")

            count += 1
            logger.info(
                f"Remaining number of iteration - {len(dict_id_pred_queries.keys())-count}"
            )

        return self

    def create_hyperparameters_table(self, hyperparameters: dict[str, Any]) -> dict[str, Any]:
        def get_params_to_log(model: Prophet, hyperparameters: list[str]) -> dict[str, Any]:
            return {hyper: getattr(model, hyper) for hyper in hyperparameters}

        return {id_pred.replace('/', '_') : get_params_to_log(model.model, list(hyperparameters.keys())) if model else None 
                for id_pred, model in self.models_dict.items()}

    def predict(self,df: pd.DataFrame,dict_id_pred_queries: dict[str, str],time_granularity: str,
                val_size: float,test_size: float = None,) -> pd.DataFrame:
        
        predictions = []
        for id_pred, query in dict_id_pred_queries.items():
            logger.info(f"START predicting {id_pred}")
            filtered_df = df.query(query)
            full_df, df_train, df_val, df_test = preprocess_and_split_df(
                self.preprocessor, filtered_df, time_granularity, val_size, test_size
            )

            model = self.models_dict[id_pred]
            if model is None:
                logger.info(
                    f"Skipping prediction for {id_pred}, as the model has not been trained"
                )
                df_output = create_zero_dataframe(
                    predict_dataframe_columns,
                    len(df_test),
                )
                df_output['Id_pred'] = id_pred
                df_output['Timestamp'] = df_test['ds']
            else:
                try:
                    df_test_pred = model.model.predict(df_test)

                    ########################################################################
                    # NON SPECIFIC MODEL SELECT # -> SPERIMENTALE
                    # Function must be preprocess_<model>_output(df: DataFrame, id_pred: str)
                    df_output = eval(f'preprocess_{self.use_model}_output(df_test_pred, id_pred)')
                    ########################################################################

                except ValueError as e:
                    logger.info(f"Skipping prediction for {id_pred}, due to: {e}")
                    df_output = create_zero_dataframe(
                        predict_dataframe_columns,
                        len(df_test),
                    )
                    df_output['Id_pred'] = id_pred
                    df_output['Timestamp'] = df_test['ds']
            # Evaluate model
            predictions.append(df_output)
            logger.info(f"DONE predicting {id_pred}")

        return pd.concat(predictions)

    def evaluate(self,df: pd.DataFrame,dict_id_pred_queries: dict[str, str],time_granularity: str,
                 val_size: float,test_size: float = None,) -> pd.DataFrame:
        
        metrics = []
        predictions = self.predict(df, dict_id_pred_queries, time_granularity, val_size, test_size)
        for id_pred, query in dict_id_pred_queries.items():
            logger.info(f"START predicting {id_pred}")
            filtered_df = df.query(query)
            full_df, df_train, df_val, df_test = preprocess_and_split_df(
                self.preprocessor, filtered_df, time_granularity, val_size, test_size
            )

            df_test.rename(columns={'ds':'Timestamp', 'y': 'Target'}, inplace=True)
            df_pred = predictions[predictions["Id_pred"] == id_pred]
            metrics.append(evaluations(df_test, df_pred, date='Timestamp' , y_true='Target', y_pred='Pred_mean'))  

        metrics = pd.concat(metrics).dropna()
        return metrics
