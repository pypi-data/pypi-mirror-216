from sklearn.base import BaseEstimator, TransformerMixin
from typing_extensions import Self, Any
import pandas as pd
from .utility.tele_logger import logger
from .utility.resources import *
from .datapreparation.datapreparation_utils import PreprocessingTeleconsulto
import pickle

class PreprocessingClass(BaseEstimator, TransformerMixin):

    def __init__(self,
                 usecase: str = "teleconsulto",
                 model: str = "prophet",
                 ):
        """Pass all the parameters that can be set as explicit keyword
        arguments.
        
        Parameters
        ----------
        usecase: str
            Parameter identifying usecase into account
        model: str
            Parameter identifying model to use
            
        """

        self.usecase = usecase
        self.model = model
        if self.usecase == "teleconsulto":
            self.preprocessing = PreprocessingTeleconsulto()
        elif self.usecase == "televisita":
            pass
        elif self.usecase == "teleassistenza":
            pass
        elif self.usecase == "telemonitoraggio":
            pass
        return
    
    @log_exception(logger)
    def fit(self,
            X: pd.DataFrame,
            y: Any = None) -> Self:
        """Learn parameters useful for transforming data.

        Parameters
        ----------
        X : pd.DataFrame
            The input DataFrame.

        y : None
            Ignored (only for compatibility).
        """

        if self.usecase == "teleconsulto":
            if self.model == "prophet":
                pass
        return self


    def transform(self,
                  X: pd.DataFrame) -> pd.DataFrame:
        """Preparing Data to feed models"

        Must be called only after calling fit method.
        Parameters
        ----------
        X : pd.DataFrame
            The input DataFrame

        Returns
        -------
        pd.DataFrame 
           DataFrame identifying the timeseries 
        """

        if self.usecase == "teleconsulto":
            if self.model == "prophet":
                X = self.preprocessing.prophet(X)
            else:
                pass
        elif self.usecase == "televisita":
            pass
        elif self.usecase == "teleassistenza":
            pass
        elif self.usecase == "telemonitoraggio":
            pass
        return X
    

    def save(self,
             path: str) -> None:
        """Store instance to file.
        Parameters
        ----------
        path : str
            Path to the file where the object must be stored.
        """

        with open(path, 'wb') as f:
            pickle.dump(self, f)
        
        return

    @classmethod
    def load(cls,
             path: str) -> Self:
        """Load instance from file.
        Parameters
        ----------
        path : str
            Path to the file where the object must be stored.
        """
        with open(path, 'rb') as f:
            return pickle.load(f)

