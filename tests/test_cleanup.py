import pytest
import pandas as pd
from klass.utility.cleanup import drop_empty_columns

@pytest.mark.parametrize(
    "input_data, expected_data",
    [
        # Case: Drops columns that are all NaN
        (pd.DataFrame({"A": [None, None], "B": [1, 2]}), pd.DataFrame({"B": [1, 2]})),
        # Case: Drops columns that are empty strings
        (pd.DataFrame({"A": ["", ""], "B": ["data", "values"]}), pd.DataFrame({"B": ["data", "values"]})),
        # Case: Mixed empty strings and NaNs
        (pd.DataFrame({"A": ["", None], "B": [1, 2]}), pd.DataFrame({"B": [1, 2]})),
        # Case: No columns dropped (all valid data)
        (pd.DataFrame({"A": ["valid", "data"], "B": [1, 2]}), pd.DataFrame({"A": ["valid", "data"], "B": [1, 2]})),
    ],
)
def test_drop_empty_columns(input_data, expected_data):
    """Tests that drop_empty_columns correctly removes empty columns."""
    result = drop_empty_columns(input_data)
    pd.testing.assert_frame_equal(result, expected_data)
