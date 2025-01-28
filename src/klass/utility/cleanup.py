import pandas as pd


def drop_empty_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Drop columns in dataset that are empty strings, or all NA.
    
    Args:
        data: The dataframe to check for columns to drop.

    Returns:
        pd.DataFrame: A modified dataframe with the empty columns removed.   
    """
    cols_na = data.isna().all()
    drop_cols = list(cols_na[cols_na].index)
    string_cols = data.select_dtypes(["object", "string"])
    for col in string_cols.columns:
        if (string_cols[col].str == ""):
            drop_cols.append(col)
    return data.drop(columns=drop_cols)        