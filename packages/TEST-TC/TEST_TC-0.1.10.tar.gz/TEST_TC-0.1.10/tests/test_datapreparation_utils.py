import pandas as pd
import numpy as np
import pytest
from tc_uc4.datapreparation.datapreparation_utils import (code_to_name, from_timestamp_to_date, generating_target,
                                                   resample_date, Normalizer, ReplacerNA, Detrender,
                                                   Deseasoner, Differencer)
from tc_uc4.utility.exceptions import InputTypeError
from statsmodels.tsa.seasonal import seasonal_decompose

### code_to_name ###

# Test case for valid input
def test_code_to_name_valid_input():
    # Create a sample pd.Series and mapping dictionary for testing
    cod = pd.Series([1, 2, 3, 4, 5])
    convers_dict = {1: "Apple", 2: "Banana", 3: "Orange", 4: "Grape", 5: "Mango"}
    # Call the code_to_name function
    result = code_to_name(cod, convers_dict)
    assert isinstance(result, pd.Series) #the result should be a Series

    expected_result = pd.Series(["Apple", "Banana", "Orange", "Grape", "Mango"])
    pd.testing.assert_series_equal(result, expected_result) #the result should has the correct value

# Test case for invalid input
def test_code_to_name_invalid_input():
    # Create an invalid input (not a pd.Series)
    invalid_cod = [1, 2, 3, 4, 5]
    convers_dict = {1: "Apple", 2: "Banana", 3: "Orange", 4: "Grape", 5: "Mango"}
    # Test for InputTypeError when invalid input is provided for cod
    with pytest.raises(InputTypeError):
        code_to_name(invalid_cod, convers_dict)

    # Create an invalid input (not a dict)
    cod = pd.Series([1, 2, 3, 4, 5])
    invalid_convers_dict = [1, 2, 3, 4, 5]
    # Test for InputTypeError when invalid input is provided for convers_dict
    with pytest.raises(InputTypeError):
        code_to_name(cod, invalid_convers_dict)


### from_timestamp_to_date ###

# Test case for valid input
def test_from_timestamp_to_date_valid_input():
    # Create a sample Series for testing
    series = pd.Series([
        pd.Timestamp("2023-01-01 10:00:00"),
        pd.Timestamp("2023-01-02 15:30:00"),
        pd.Timestamp("2023-01-03 08:45:00")
    ])
    # Call the from_timestamp_to_date function
    result = from_timestamp_to_date(series)
    assert isinstance(result, pd.Series) #the result should be a Series
    assert result.dtype == "datetime64[ns]" #the results should has a datetime type

 
    expected_result = pd.Series([
        pd.Timestamp("2023-01-01"),
        pd.Timestamp("2023-01-02"),
        pd.Timestamp("2023-01-03")
    ])
    pd.testing.assert_series_equal(result, expected_result) #the result should has the correct value


# Test case for invalid input
def test_from_timestamp_to_date_invalid_input():
    # Create an invalid input (not a Series)
    invalid_input = "2023-01-01 10:00:00"
    # Test for InputTypeError when invalid input is provided
    with pytest.raises(InputTypeError):
        from_timestamp_to_date(invalid_input)

    # Create an invalid input (Series with non-datetime dtype)
    series_with_invalid_dtype = pd.Series(["2023-01-01", "2023-01-02", "2023-01-03"])
    # Test for TypeError when input Series has non-datetime dtype
    with pytest.raises(TypeError):
        from_timestamp_to_date(series_with_invalid_dtype)


### generating_target ###

# Test case for valid inputs
def test_generating_target_valid_inputs():
    # Create a sample DataFrame for testing
    df = pd.DataFrame({
        "col1": [1, 1, 2, 2],
        "col2": [3, 3, 4, 4],
        "target": [5, 5, 6, 6]
    })

    # Specify the column index and target column
    col_index = ["col1", "col2"]
    target_col = "target"
    # Call the generating_target function
    result = generating_target(df, col_index, target_col)
    assert isinstance(result, pd.DataFrame) #the result should be a DataFrame

    expected_columns = col_index + [target_col]
    assert result.columns.tolist() == expected_columns # the result should has the correct columns

    expected_result = pd.DataFrame({
        "col1": [1, 2],
        "col2": [3, 4],
        "target": [2, 2]
    })
    pd.testing.assert_frame_equal(result, expected_result) #the result should has the correct values

# Test case for invalid inputs
def test_generating_target_invalid_inputs():
    # Create a sample DataFrame for testing
    df = pd.DataFrame({
        "col1": [1, 1, 2, 2],
        "col2": [3, 3, 4, 4],
        "target": [5, 5, 6, 6]
    })

    # Specify invalid column index (not a list)
    invalid_col_index = "col1"
    # Specify invalid target column (not a string)
    invalid_target_col = 123
    # Test for InputTypeError when invalid inputs are provided
    with pytest.raises(InputTypeError):
        generating_target(df, invalid_col_index, "target")
    with pytest.raises(InputTypeError):
        generating_target(df, ["col1", "col2"], invalid_target_col)

    # Test for missing columns in the DataFrame
    with pytest.raises(InputTypeError):
        generating_target(df, ["col1", "col3"], "target")
    with pytest.raises(InputTypeError):
        generating_target(df, ["col1", "col2"], "missing_col")
    with pytest.raises(InputTypeError):
        generating_target(df, ["col1", "col3"], "missing_col")


### resample_date ###

# Test case for valid input
def test_resample_date_valid_input():
    # Create a sample DataFrame for testing
    df = pd.DataFrame({
        "Timestamp": pd.date_range("2022-01-01", "2022-01-10"),
        "Value": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    })
    # Call the resample_date function
    result = resample_date(df)
    assert isinstance(result, pd.DataFrame) #the result should be a DataFrame
    expected_rows = 10
    assert len(result) == expected_rows #the results should has the correct number of rows
    expected_columns = ["Timestamp", "Value"]
    assert list(result.columns) == expected_columns #the results should has the correct columns

# Test case for invalid input
def test_resample_date_invalid_input():
    # Create an invalid input (not a pd.DataFrame)
    invalid_df = [1, 2, 3, 4, 5]
    # Test for InputTypeError when invalid input is provided for df
    with pytest.raises(InputTypeError):
        resample_date(invalid_df)

    # Create an invalid input (datetime_col is not a string)
    df = pd.DataFrame({
        "Timestamp": pd.date_range("2022-01-01", "2022-01-10"),
        "Value": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    })
    invalid_datetime_col = 123
    # Test for InputTypeError when invalid input is provided for datetime_col
    with pytest.raises(InputTypeError):
        resample_date(df, datetime_col=invalid_datetime_col)

    # Create an invalid input (grouping_cols is not a list or None)
    invalid_grouping_cols = "invalid"
    # Test for InputTypeError when invalid input is provided for grouping_cols
    with pytest.raises(InputTypeError):
        resample_date(df, grouping_cols=invalid_grouping_cols)

    # Create an invalid input (target is not a string)
    invalid_target = ["invalid"]
    # Test for InputTypeError when invalid input is provided for target
    with pytest.raises(InputTypeError):
        resample_date(df, target=invalid_target)

    # Create an invalid input (s is not a string)
    invalid_s = 123
    # Test for InputTypeError when invalid input is provided for s
    with pytest.raises(InputTypeError):
        resample_date(df, s=invalid_s)


### Normalizer ###

@pytest.fixture
def example_data():
    # Example data for testing
    data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                         'volumes': [10, 20, 30, 40, 50]})
    return data

def test_fit_normalizer(example_data):
    # Create an instance of the Normalizer class
    normalizer = Normalizer()

    # Call the fit method with the example data
    fitted_normalizer = normalizer.fit(example_data)

    # Verify that the output is the same instance of normalizer
    assert fitted_normalizer is normalizer

    # Verify that the min and max values are calculated correctly
    assert normalizer.min == 10
    assert normalizer.max == 50

def test_transform_normalizer(example_data):
    # Create an instance of the Normalizer class
    normalizer = Normalizer()

    # Call the fit method with the example data
    normalizer.fit(example_data)

    # Call the transform method with the example data
    transformed_data = normalizer.transform(example_data)
    print(transformed_data)

    # Verify that the output is a DataFrame
    assert isinstance(transformed_data, pd.DataFrame)

    # Verify that the DataFrame has the correct columns
    assert transformed_data.columns.tolist() == ['timestamp', 'volumes']

    # Verify that the data is correctly normalized
    assert transformed_data['volumes'].min() == 0
    assert transformed_data['volumes'].max() == 1

    # Verify that the data has not been modified in other ways
    assert example_data['timestamp'].equals(transformed_data['timestamp'])


### ReplacerNA ###

#transform function
@pytest.fixture
def example_data_transform():
    # Example data for testing
    data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                         'volumes': [10, None, 30, None, 50]})
    return data

def test_fit_replace_na(example_data_transform):
    # Create an instance of the ReplacerNA class with method="mean"
    replacer = ReplacerNA(method="mean")

    # Call the fit method with the example data
    fitted_replacer = replacer.fit(example_data_transform)

    # Verify that the output is the same instance of replacer
    assert fitted_replacer is replacer

    # Verify that the value and method_for_df are calculated correctly
    assert replacer.value == 30.0
    assert replacer.method_for_df is None

def test_transform_replace_na(example_data_transform):
    # Create an instance of the ReplacerNA class with method="zero"
    replacer = ReplacerNA(method="zero")

    # Call the fit method with the example data
    replacer.fit(example_data_transform)

    # Call the transform method with the example data
    transformed_data = replacer.transform(example_data_transform)
    print(transformed_data)
    # Verify that the output is a DataFrame
    assert isinstance(transformed_data, pd.DataFrame)

    # Verify that the transformed data has missing values replaced correctly
    expected_data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                                  'volumes': [10.0, 0.0, 30.0, 0.0, 50.0]})
    pd.testing.assert_frame_equal(transformed_data, expected_data)

def test_transform__replace_na_ffill(example_data_transform):
    # Create an instance of the ReplacerNA class with method="ffill"
    replacer = ReplacerNA(method="ffill")

    # Call the fit method with the example data
    replacer.fit(example_data_transform)

    # Call the transform method with the example data
    transformed_data = replacer.transform(example_data_transform)

    # Verify that the transformed data has missing values replaced correctly using forward fill
    expected_data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                                  'volumes': [10.0, 10.0, 30.0, 30.0, 50.0]})
    pd.testing.assert_frame_equal(transformed_data, expected_data)


### Detrender ###

#trend function
@pytest.fixture
def example_data_trend():
    # Example data for testing
    data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                         'volumes': [10, 20, 30, 40, 50]})
    return data

def test_fit_detrender(example_data_trend):
    # Create an instance of the Detrender class with period=2
    detrender = Detrender(period=2)

    # Call the fit method with the example data
    fitted_detrender = detrender.fit(example_data_trend)

    # Verify that the output is the same instance of detrender
    assert fitted_detrender is detrender

    # Verify that the trend is calculated correctly
    expected_trend = pd.Series([10.0, 20.0, 30.0, 40.0, 50.0], name='trend')
    pd.testing.assert_series_equal(detrender.trend, expected_trend)

def test_transform_detrender(example_data_trend):
    # Create an instance of the Detrender class with period=2
    detrender = Detrender(period=2)

    # Call the fit method with the example data
    detrender.fit(example_data_trend)

    # Call the transform method with the example data
    transformed_data = detrender.transform(example_data_trend)

    # Verify that the output is a DataFrame
    assert isinstance(transformed_data, pd.DataFrame)

    # Verify that the transformed data is detrended correctly
    expected_trend = seasonal_decompose(example_data_trend['volumes'], model='additive', period=2, extrapolate_trend='freq').trend
    expected_data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                                  'volumes': example_data_trend['volumes'] - expected_trend})
    pd.testing.assert_frame_equal(transformed_data, expected_data)


### Deseasoner ###

#season function
@pytest.fixture
def example_data_season():
    # Example data for testing
    data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                         'volumes': [10, 20, 30, 40, 50]})
    return data

def test_transform_deseasoner(example_data_season):
    # Create an instance of the Deseasoner class with period=2
    deseasoner = Deseasoner(period=2)

    # Call the fit method with the example data
    deseasoner.fit(example_data_season)

    # Call the transform method with the example data
    transformed_data = deseasoner.transform(example_data_season)

    # Verify that the output is a DataFrame
    assert isinstance(transformed_data, pd.DataFrame)

    # Verify that the transformed data is deseasonalized correctly
    expected_seasonal = seasonal_decompose(example_data_season['volumes'], model='additive', period=2, extrapolate_trend='freq').seasonal
    expected_data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                                  'volumes': example_data_season['volumes'] - expected_seasonal})
    pd.testing.assert_frame_equal(transformed_data, expected_data)


### Differencer ###

#difference function
@pytest.fixture
def example_data_difference():
    # Example data for testing
    data = pd.DataFrame({'timestamp': [1, 2, 3, 4, 5],
                         'volumes': [10, 20, 30, 40, 50]})
    return data

def test_transform_differencer(example_data_difference):
    # Create an instance of the Differencer class with lag=1
    differencer = Differencer(lag=1)

    # Call the fit method with the example data
    differencer.fit(example_data_difference)

    # Call the transform method with the example data
    transformed_data = differencer.transform(example_data_difference)

    # Verify that the output is a DataFrame
    assert isinstance(transformed_data, pd.DataFrame)

    # Verify that the transformed data is differenced correctly
    expected_data = pd.DataFrame({'timestamp': [2, 3, 4, 5],
                                  'volumes': [10, 10, 10, 10]})
    pd.testing.assert_frame_equal(transformed_data, expected_data)
