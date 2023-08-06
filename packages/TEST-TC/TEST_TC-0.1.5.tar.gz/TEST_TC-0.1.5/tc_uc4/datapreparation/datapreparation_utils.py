import pandas as pd
from tc_uc4.utility.tele_logger import logger
from tc_uc4.utility.exceptions import InputTypeError
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.base import BaseEstimator, TransformerMixin
from typing_extensions import Self
from typing import Union, Dict, List

class PreprocessingTeleconsulto:

    def prophet(self,
                df: pd.DataFrame) -> pd.DataFrame:
        
        """
        Sequential execution of transformations to obtain a DataFrame with a time series structure

        Returns:
            pd.DataFrame: DataFrame identifying the timeseries generated according to specified hierarchies and time span
        """
        # Raw dataset from which to generate the time serie
        self.df = df.copy()
        # column name identifying the columns to index on
        self.datetime_index = "data_richiesta"
        # column name identifying column from which to generate target
        self.target = "id_teleconsulto"

         # Verify that df is of type pd.DataFrame
        if not isinstance(df, pd.DataFrame):
            logger.info("Input 'df' must be of type pd.DataFrame", important=True)
            raise InputTypeError('datapreparation_utils.prophet')
        # Verify that datetime_index is a non-empty string and a column in df
        if  self.datetime_index not in df.columns:
            logger.info("Invalid value for 'datetime_index'. It must be a column in 'df'", important=True)
            raise InputTypeError('datapreparation_utils.prophet')
        # Verify that target is a non-empty string and a column in df
        if self.target not in df.columns:
            logger.info("Invalid value for 'target'. It must be a column in 'df'", important=True)
            raise InputTypeError('datapreparation_utils.prophet')

        logger.info('Starting preparing data', important = True)
        
        logger.info('Extracting date from datetime column')
        self.df["Timestamp"] = from_timestamp_to_date(self.df[self.datetime_index])

        logger.info('Generating the timeseries target')
        self.df_target = generating_target(self.df, ["Timestamp"],self.target)

        logger.info('Creating the entire timeline to complete the target')
        self.df_calendar = pd.DataFrame(resample_date(self.df_target, "Timestamp",target=self.target))['Timestamp']
            
        df_ts = pd.merge(self.df_calendar, self.df_target, how='left', on="Timestamp")
        logger.info('Generating the complete timeseries', important = True)
        df_ts.rename(columns={self.target:'Target'}, inplace=True)

        return df_ts
    


def code_to_name(cod: pd.Series, convers_dict: Dict) -> pd.Series:
    
    """
    The function generates a new column converting the code number into a meaningful string

    Parameters
    ----------
    cod: pd.Series
       The code number column
    convers_dict: dict
        The mapping dictionary from code to string

    Returns
    -------
        pd.Series
        Returns the modified column based on the mapping dictionary
    """
    if not isinstance(cod, pd.Series):
        logger.info("Input 'cod' must be of type pd.Series")
        raise InputTypeError('datapreparation_utils.cod_to_name')
    if not isinstance(convers_dict, dict):
        logger.info("Input 'convers_dict' must be of type dict")
        raise InputTypeError('datapreparation_utils.cod_to_name')
                  
    return cod.apply(lambda i: convers_dict[int(i)])


def from_timestamp_to_date(df: pd.Series) -> pd.Series:
        """  
        Extract the date from datetime

        Parameters
        ----------
        df: pandas.Series 
            Pandas.series object identifying datetime to convert

        Returns
        -------
        to_date: pandas.Series 
            pandas.Series datetime64[ns] object identifying date

        """  
        #Verify that df is of type pd.Series
        if not isinstance(df, pd.Series):
            logger.info("Input df must be a pandas.Series")
            raise(InputTypeError('datapreparation_utils.from_timestamp_to_date'))
        #verify that df is a pandas.Series of type datetime
        if not pd.api.types.is_datetime64_any_dtype(df.dtype):
            logger.info("Input df must be of type datetime")
            raise TypeError("Input df must be of type datetime")
       
        to_date = pd.to_datetime(df.dt.date)
        return to_date

def generating_target(df: pd.DataFrame,
                      col_index: List,
                      target_col: str) -> pd.DataFrame:
        
        """ Creates the timeseries target

        Parameters
        ----------
        df: pd.DataFrame
            DataFrame with the fixed ennuple and date column used to generate timeseries 

        col_index: list
            column names identifying the columns to aggregate on

        target_col: str
            column name identifying the target (e.g.: id_teleconsulto)

        Returns
        -------
        grouped_df: pd.DatFrame 
            Dataframe with the aggregation

        """
        
         # Verify that df is of type pd.DataFrame
        if not isinstance(df, pd.DataFrame):
            logger.info("Input 'df' must be of type pd.DataFrame")
            raise(InputTypeError('datapreparation_utils.generating_target'))

        # Verify that col_index is a non-empty list
        if not isinstance(col_index, list) or len(col_index) == 0:
            logger.info("Input 'col_index' must be a non-empty list")
            raise(InputTypeError('datapreparation_utils.generating_target'))

         # Verify that elements in col_index are non-empty strings 
        if not all(isinstance(col, str) and len(col) > 0 for col in col_index):
            logger.info("Elements in 'col_index' must be non-empty strings")

        # Verify that target_col is a non-empty string
        if not isinstance(target_col, str) or len(target_col) == 0:
            logger.info("Input 'target_col' must be a non-empty string")
            raise(InputTypeError('datapreparation_utils.generating_target'))
        
        # Verify that columns in col_index exist in df
        missing_columns = [col for col in col_index if col not in df.columns]
        if missing_columns:
            logger.info(f"The following columns are missing in 'df': {', '.join(missing_columns)}")
            raise(InputTypeError('datapreparation_utils.generating_target'))

        # Verify that che target_col is a df column
        if target_col not in df.columns:
            logger.info(f"Column '{target_col}' is missing in 'df'")
            raise(InputTypeError('datapreparation_utils.generating_target'))

        grouped_df = df.groupby(col_index).agg({target_col:"count"}).reset_index()

        return grouped_df

def resample_date(df: pd.DataFrame,
                  datetime_col : str = "Timestamp",
                  grouping_cols : List = [None],
                  target : str = "Target",
                  s: str = "D") -> pd.DataFrame:

        """Creates the entire daily time series in a fixed datetime range 

        Parameters
        ----------
        df: pd.DataFrame
           pandas DataFrame from which resample time-series data
        datetime_col: str
           column on which to insert missing dates
        grouping_cols: list
           list of columns specifying a hierarchy. If None, no hierarchy should be considered
        target: str
           column identifying target column 
        s: str
            Date Offset to consider, tipically "D" (daily), "W" (weekly), "M" (monthly)

        Returns
        -------
        s: pd.DataFrame 
           Resampled time-series data

        """
        
        # Verify that "df" is a pd.DataFrame
        if not isinstance(df, pd.DataFrame):
            logger.info("Input 'df' must be of type pd.DataFrame")
            raise(InputTypeError('datapreparation_utils.resample_date'))
        
        # Verify that datetime_col is a non-empty string
        if not isinstance(datetime_col, str) or len(datetime_col) == 0:
            logger.info("Input 'datetime_col' must be a non-empty string")
            raise(InputTypeError('datapreparation_utils.resample_date'))
        
        # Verify that grouping_cols is either a list or None
        if grouping_cols !=[None] and not isinstance(grouping_cols, list):
            logger.info("Input 'grouping_cols' must be a list or None")
            raise(InputTypeError('datapreparation_utils.resample_date'))
        
        # Verify that columns in grouping_cols exist in df
        if grouping_cols !=[None]:
            print(grouping_cols)
            if not all(col in df.columns for col in grouping_cols):
                logger.info("Columns in 'grouping_cols' must exist in the DataFrame")
                raise(InputTypeError('datapreparation_utils.resample_date'))
        
        # Verify that target is a non-empty string
        if not isinstance(target, str) or len(target) == 0:
            logger.info("Input 'target' must be a non-empty string")
            raise(InputTypeError('datapreparation_utils.resample_date'))

        # Verify that s is a non-empty string
        if not isinstance(s, str) or len(s) == 0:
            logger.info("Input 's' must be a non-empty string")
            raise(InputTypeError('datapreparation_utils.resample_date'))
        
        # Verify that datetime_col is a dataframe column of type pd.Datetime 
        if datetime_col not in df.columns or not pd.api.types.is_datetime64_any_dtype(df[datetime_col].dtype):
            logger.info("Input 'datetime_col' must be a column of type pd.Datetime")


        if grouping_cols==[None]:
            output = df.set_index(datetime_col).resample(s.title()).sum().reset_index()
        else:
            output = df.set_index(datetime_col).groupby(grouping_cols)[target].apply(lambda x: x.asfreq(s.title()))

        return output


class Normalizer(TransformerMixin, BaseEstimator):

    """Normalization class for time series (between 0 and 1)
    """

    def __init__(self):
        pass

    def fit(self, X: pd.DataFrame) -> Self:

        """Compute value min and max useful to normalize data

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            fitted normalizer
        """

        self.min = X.iloc[:,1].min()
        self.max = X.iloc[:,1].max()

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """Perform normalization between 0 and 1

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            transformed time series
        """

        normalized = (X.iloc[:,1] - self.min) / (self.max - self.min)
        ris = pd.concat([X.iloc[:,0],normalized],axis=1)
        ris.columns = X.columns
        
        return ris
    
class ReplacerNA(TransformerMixin, BaseEstimator):

    def __init__(self, method: Union[str,int] = 0) -> Self:

        """class for handling of NA

        Parameters
        ----------
        method : str | int
            if str specify the method to replace NA value (mean,median,zero), if int specify the value to replace NA value

        Returns
        -------
        self : object
        """
        
        self.method = method

    def fit(self, X: pd.DataFrame) -> Self:

        """Compute value useful for replacing NA

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            fitted replacer
        """
        
        if self.method == "mean":
            self.value = X.iloc[:,1].mean()
            self.method_for_df = None
        elif self.method == "median":
            self.value = X.iloc[:,1].median()
            self.method_for_df = None
        elif self.method == "zero":
            self.value = 0
            self.method_for_df = None
        elif self.method == "bfill":
            self.value = None
            self.method_for_df = "bfill"
        elif self.method == "ffill":
            self.value = None
            self.method_for_df = "ffill"
        else:
            self.value = self.method
            self.method_for_df = None

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """Perform replacement of missing values

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            transformed time series
        """
         
        return X.fillna(self.value, method=self.method_for_df)
    
class Detrender(TransformerMixin, BaseEstimator):

    def __init__(self, period: int) -> Self:

        """Detrending time series

        Parameters
        ----------
        period : int
            specify period considered for compute additive decomposition

        Returns
        -------
        self : object
        """

        self.period = period


    def fit(self, X: pd.DataFrame) -> Self:

        """Compute additive decomposition useful to detrend time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            fitted detrender
        """

        additive_decomp = seasonal_decompose(X.iloc[:,1], model="additive", period=self.period, extrapolate_trend="freq")
        self.trend = additive_decomp.trend

        return self

    def transform(self, X:pd.DataFrame) -> pd.DataFrame:

        """Perform detrending of time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            transformed time series
        """

        detrend_time_series = X.iloc[:,1] - self.trend
        ris = pd.concat([X.iloc[:,0],detrend_time_series],axis=1)
        ris.columns = X.columns

        return  ris
    
class Deseasoner(TransformerMixin, BaseEstimator):

    def __init__(self, period: int) -> Self:

        """Deseasonalises time series

        Parameters
        ----------
        period : int
            specify period considered for compute additive decomposition

        Returns
        -------
        self : object
        """

        self.period = period


    def fit(self, X: pd.DataFrame) -> Self:

        """Compute additive decomposition useful to deseasonalises time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            fitted deseasoner
        """
        
        additive_decomp = seasonal_decompose(X.iloc[:,1], model="additive", period=self.period, extrapolate_trend="freq")
        self.seasonal = additive_decomp.seasonal

        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """Perform deseasonalises of time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            transformed time series
        """

        deseason_time_series = X.iloc[:,1] - self.seasonal
        ris = pd.concat([X.iloc[:,0],deseason_time_series],axis=1)
        ris.columns = X.columns

        return ris

class Differencer(TransformerMixin, BaseEstimator):

    def __init__(self, lag: int) -> Self:

        """Differencing time series
        
        Parameters
        ----------
        lag : int
            differencing time series lag

        Returns
        -------
        self : object
        """

        self.lag = lag

    def fit(self, X: pd.DataFrame) -> Self:

        """Compute value useful to compute differencing time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)         

        Returns
        -------
        self : object
            fitted normalizer
        """

        self.shape = X.shape[0]
        self.lag_time_series = X.iloc[:self.shape-self.lag,1]
        self.timestamp = X.iloc[self.lag:,0].reset_index(drop=True)

        return self
    
    def transform(self, X: pd.DataFrame) -> pd.DataFrame:

        """Perform differencing time series

        Parameters
        ----------
        X : pd.DataFrame
            dataframe containing two columns (timestamp and volumes of time series)

        Returns
        -------
        X : pd.DataFrame
            transformed time series
        """

        time_series_lagged = X.iloc[self.lag:,1].reset_index(drop=True) - self.lag_time_series
        ris = pd.concat([self.timestamp,time_series_lagged], axis=1)
        ris.columns = X.columns
        
        return ris
     
