import numpy as np
import pandas as pd

from tc_uc4.utility.constants import code_to_region_name, code_to_speciality


def add_mapped_columns(
    hierarchy: dict[str, str], df: pd.DataFrame, conversion: dict[str, str]
) -> tuple[pd.DataFrame, dict[str, str]]:
    """Adds columns in the dataframe "df" according to a given hierarchy and conversion dictionary.

    Parameters
    ----------
    hierarchy : dict[str, str]
        A dictionary mapping levels to column names in the DataFrame.
    df : pd.DataFrame
        The input DataFrame to be mapped.
    conversion : dict[str, str]
        A dictionary mapping levels to conversion names.

    Returns
    -------
    tuple[pd.DataFrame, dict[str, str]]
        A tuple containing the modified DataFrame and the updated hierarchy dictionary.
    """
    for conversion_level in conversion.keys():
        if conversion[conversion_level]:
            name_column = hierarchy[conversion_level]
            dict_mapping = eval(conversion[conversion_level])
            df[name_column + "_mapped"] = df[name_column].apply(
                lambda x: dict_mapping[x]
            )
            hierarchy[conversion_level] = name_column + "_mapped"
    return df, hierarchy


def generate_queries(hierarchy_values: list[str], df: pd.DataFrame) -> dict[str, str]:
    """Generate a dictionary of ids and queries based on the given hierarchy values and DataFrame.

    Parameters
    ----------
    hierarchy_values : list[str]
        A list of hierarchy levels in the DataFrame.
    df : pd.DataFrame
        The DataFrame containing the data.


    Returns
    -------
    dict[str, str]
        Dictionary where the keys are unique identifiers and the values are queries.
    """
    dictionary = {}
    for n in range(1, len(hierarchy_values) + 1):
        df_aggregate = df.loc[:, hierarchy_values[:n]].drop_duplicates()
        for i in df_aggregate.itertuples(index=False):
            query = str(i)[6:].replace("=", "==").replace(",", " &")
            id_pred = "/".join([f"{i[j]}" for j in range(len(i))])
            dictionary[id_pred] = query
    return dictionary


def create_zero_dataframe(columns: list[str], n_rows: int) -> pd.DataFrame:
    """Creates a dataframe with the given columns and rows full of zeros.

    Parameters
    ----------
    columns : list[str]
        column names
    n_rows : int
        Number of rows

    Returns
    -------
    pd.DataFrame
        dataframe
    """
    # Create a dictionary with the column names and values
    data = {col: np.zeros(n_rows) for col in columns}

    # Create the dataframe
    df = pd.DataFrame(data)

    return df
