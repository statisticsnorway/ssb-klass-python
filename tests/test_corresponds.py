import pandas as pd


def test_correspondance_data_length(
    klass_correspondance_success,
):
    version_data = klass_correspondance_success.data
    assert len(version_data)
    assert isinstance(version_data, pd.DataFrame)
