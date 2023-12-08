import pandas as pd


def test_correspondence_data_length(
    klass_correspondence_from_id_success,
):
    version_data = klass_correspondence_from_id_success.data
    assert len(version_data)
    assert isinstance(version_data, pd.DataFrame)


def test_correspondence_has_str_repr(klass_correspondence_from_id_success):
    assert klass_correspondence_from_id_success.__str__()
    assert klass_correspondence_from_id_success.__repr__()
    assert len(klass_correspondence_from_id_success.__str__())
    assert len(klass_correspondence_from_id_success.__repr__())


def test_correspondence_can_contain_quarter(
    klass_correspondence_between_classifications_success,
):
    short = klass_correspondence_between_classifications_success
    assert isinstance(short.from_date, str)
    assert len(short.from_date)
    short.contain_quarter = 3
    short.to_date = short._last_date_of_quarter()
    assert short.to_date[-5:] == "09-30"
