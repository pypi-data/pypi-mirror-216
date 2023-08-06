import warnings;
warnings.simplefilter('ignore')
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error , r2_score, mean_absolute_error
from ..utility.exceptions import ColumnNotFound
from ..utility.tele_logger import logger


def evaluations(df_real: pd.DataFrame, df_pred: pd.DataFrame, date: str = 'Timestamp' , y_true: str = 'Target', y_pred: str = 'Pred_mean') -> pd.DataFrame:
    """
    Create a DataFrame representing the evaluation metrics

    Parameters
    ----------
    df_real: pd.DataFrame
        the dataframes containing the real values
    df_pred: pd.DataFrame
        the dataframes containing the predicted values
    date: str
        the column name for the timestamp
    y_true: str
        the target column name for the real datasets
    y_pred: str
        the target column name for the predict datasets

    Returns
    -------
        A pd.DataFrame containing the results for MAE, RMSE, MSE and R2
    """
    if date not in df_real.columns:
        raise ColumnNotFound(func='evaluations', column=date, data=df_real)
    if date not in df_pred.columns:
        raise ColumnNotFound(func='evaluations', column=date, data=df_pred)
    if y_true not in df_real.columns:
        raise ColumnNotFound(func='evaluations', column=y_true, data=df_real)
    if y_pred not in df_pred.columns:
        raise ColumnNotFound(func='evaluations', column=y_pred, data=df_pred)

    logger.info('START Ealuating results')

    df_real= df_real.set_index(date).dropna()
    df_pred= df_pred.set_index(date).dropna()
    inter = df_real.index.intersection(df_pred.index)

    if len(inter) == 0:
        raise Exception('Length of intersection between Predictions and Ground Truth Datasets is Null. Probably one of the two Datasets has not available data (all NaN).')

    df_real = df_real.loc[inter]
    df_pred = df_pred.loc[inter]

    # Mean Absolute Error
    logger.info('Evaluating MAE')
    mae = round(mean_absolute_error(df_real[y_true], df_pred[y_pred]),2)
    # Root Mean Square Error
    logger.info('Evaluating RMSE')
    rmse = round(mean_squared_error(df_real[y_true], df_pred[y_pred], squared = False),2)
    # Mean Square Error
    logger.info('Evaluating MSE')
    mse = round(mean_squared_error(df_real[y_true], df_pred[y_pred]),2)
    # Coefficient of Determination
    logger.info('Evaluating R2')
    r2 = round(r2_score(df_real[y_true], df_pred[y_pred]),2)

    scores = {'MAE':mae,'RMSE': rmse, 'MSE':mse, 'R2':r2}
    scoreType = list(scores.keys())
    scoreValues = list(scores.values())
    # Saving the scores in a DF
    ev_matrix = pd.DataFrame(list(zip(scoreType, scoreValues)), columns =['Metrics', 'Value'])

    logger.info('DONE Evaluating results')

    return ev_matrix
