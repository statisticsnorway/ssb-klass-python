from typing import Final
from typing import Literal
from typing import cast

import pandas as pd

STRING_DTYPE: Final[Literal["string[pyarrow]"]] = "string[pyarrow]"


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
        non_empty = (
            limit_data[[key, value]].astype(STRING_DTYPE).fillna("") != ""
        ).all(axis=1)
        mask = cast(pd.Series, limit_data[[key, value]].notna().all(axis=1) & non_empty)
        limit_data = limit_data.loc[mask]
        print(limit_data)
    if select_level:
        level_mask = cast(
            pd.Series,
            limit_data["level"].astype(STRING_DTYPE) == str(select_level),
        )
        limit_data = limit_data.loc[level_mask]
    return limit_data


def apply_presentation_name_fallback(
    df: pd.DataFrame,
    value: str,
    fallback: str = "name",
    fallback_col: str = "_value_fallback",
) -> tuple[pd.DataFrame, str]:
    """Create a fallback value column when presentation names are empty.

    Args:
        df: Input DataFrame.
        value: The value column name requested.
        fallback: The fallback column name to use when presentation names are empty.
        fallback_col: The name of the temporary column to store the fallback result.

    Returns:
        tuple[pd.DataFrame, str]: The DataFrame (possibly augmented) and the effective value column name.
    """
    if value != "presentationName" or fallback not in df.columns:
        return df, value
    data = df.copy()
    data[fallback_col] = data["presentationName"].astype(STRING_DTYPE).fillna("")
    empty_mask = cast(pd.Series, data[fallback_col] == "")
    if empty_mask.any():
        data.loc[empty_mask, fallback_col] = data[fallback].astype(STRING_DTYPE)
    return data, fallback_col
