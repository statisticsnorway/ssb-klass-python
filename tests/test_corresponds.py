import pandas as pd


def test_correspondence_data_length(
    klass_correspondence_from_id_success,
):
    version_data = klass_correspondence_from_id_success.data
    assert len(version_data)
    assert isinstance(version_data, pd.DataFrame)


def test_correspondence_has_str_repr(klass_correspondence_from_id_success):
    klass_correspondence_from_id_success.correspondence_id = "100"
    klass_correspondence_from_id_success.source_classification_id = "200"
    klass_correspondence_from_id_success.target_classification_id = "300"
    klass_correspondence_from_id_success.from_date = "2023-01-01"
    klass_correspondence_from_id_success.to_date = "2023-01-01"
    klass_correspondence_from_id_success.language = "nn"
    assert klass_correspondence_from_id_success.__str__()
    assert klass_correspondence_from_id_success.__repr__()
    assert len(klass_correspondence_from_id_success.__str__())
    assert len(klass_correspondence_from_id_success.__repr__())
    print(klass_correspondence_from_id_success)
    repr(klass_correspondence_from_id_success)


def test_correspondence_can_contain_quarter(
    klass_correspondence_between_classifications_success,
):
    short = klass_correspondence_between_classifications_success
    assert isinstance(short.from_date, str)
    assert len(short.from_date)
    short.contain_quarter = 3
    short.to_date = short._last_date_of_quarter()
    assert short.to_date[-5:] == "09-30"


def test_correspondence_to_dict(klass_correspondence_between_classifications_success):
    result = klass_correspondence_between_classifications_success.to_dict()
    assert isinstance(result, dict)
    assert len(result)
