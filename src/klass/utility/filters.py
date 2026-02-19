import pandas as pd


def limit_na_level(
    df: pd.DataFrame,
    key: str,
    value: str,
    remove_na: bool = True,
    select_level: int | None = None,
) -> pd.DataFrame:
    """Filter a correspondence DataFrame by NA/empty values and optional level.

    Creates a filtered copy of the input DataFrame where rows may be removed
    based on missing or empty values in the specified key/value columns and/or
    restricted to a specific classification level.

    If ``remove_na`` is True, rows are kept only if both ``key`` and ``value``:
    - are not NA
    - are not empty strings (after string conversion)

    If ``select_level`` is provided, only rows where the ``level`` column
    matches the given value are retained.

    Args:
        df: The input DataFrame containing correspondence data.
        key: Column name used as dictionary keys in downstream mapping.
        value: Column name used as dictionary values in downstream mapping.
        remove_na: Whether to remove rows where key/value are NA or empty strings.
        select_level: Optional classification level to filter on.

    Returns:
        pd.DataFrame: A filtered copy of the input DataFrame.
    """
    limit_data = df.copy()
    if remove_na:
        print(key, value)
        mask = limit_data[[key, value]].notna().all(axis=1) & (
            limit_data[[key, value]].astype("string[pyarrow]").fillna("") != ""
        ).all(axis=1)
        limit_data = limit_data[mask]
        print(limit_data)
    if select_level:
        limit_data = limit_data[
            limit_data["level"].astype("string[pyarrow]") == str(select_level)
        ]
    return limit_data
