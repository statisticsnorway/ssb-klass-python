import pandas as pd


def test_correspondence_data_length(
    klass_correspondence_success,
):
    version_data = klass_correspondence_success.data
    assert len(version_data)
    assert isinstance(version_data, pd.DataFrame)


def test_correspondence_has_str_repr(klass_correspondence_success):
    assert klass_correspondence_success.__str__()
    assert klass_correspondence_success.__repr__()
    assert len(klass_correspondence_success.__str__())
    assert len(klass_correspondence_success.__repr__())
