import pandas as pd


def test_correspondence_data_length(
    klass_correspondence_success,
):
    version_data = klass_correspondence_success.data
    assert len(version_data)
    assert isinstance(version_data, pd.DataFrame)
