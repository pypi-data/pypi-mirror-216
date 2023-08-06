import pandas as pd
import numpy as np
import pytest
from analytics.evaluationMetrics import evaluations
from utility.exceptions import ColumnNotFound

def test_evaluations():
     # Sample data 
     real_df = pd.DataFrame({'Timestamp': [1, 2, 3], 'Target': [10, 20, 30]})
     prophet_df = pd.DataFrame({'Timestamp': [1, 2, 3], 'Pred_mean': [12, 18, 32]})

     # Calculate evaluation metrics
     result = evaluations(real_df, prophet_df)

     # Verify the content of the evaluation dataframe
     assert isinstance(result, pd.DataFrame)  # The result should be a DataFrame
     assert len(result) == 4  # The DataFrame should have 4 rows
     assert set(result.columns) == {'Metrics', 'Value'}  # The DataFrame should have the correct columns
     assert result['Metrics'].tolist() == ['MAE', 'RMSE', 'MSE', 'R2']  # The values in the 'Metrics' column should be correct
     assert result['Value'].tolist() == [2.0, 2.0, 4.0, 0.94]  # The values in the 'Value' column should be correct

     prophet_df = pd.DataFrame({'Timestamp': [1, 2, 3], 'Pred_mean': [np.nan, np.nan, np.nan]})
     with pytest.raises(Exception):
         evaluations(real_df, prophet_df)

def test_evaluations_column_not_found():
    # Sample data without the 'Pred_mean' column in the pred dataframe
     df_real = pd.DataFrame({'Timestamp': [1, 2, 3], 'Target': [10, 20, 30]})
     df_pred = pd.DataFrame({'Timestamp': [1, 2, 3], 'Value': [12, 18, 32]})

     # Sample data without the 'Timestamp' column in the real dataframe
     df_real2 = pd.DataFrame({'timestamp': [1, 2, 3], 'Target': [10, 20, 30]})

     # Check if the ColumnNotFound exception is raised
     with pytest.raises(ColumnNotFound):
          evaluations(df_real, df_pred)
     
     with pytest.raises(ColumnNotFound):
          evaluations(df_real2, df_pred)
