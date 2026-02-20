from unittest import mock

import pandas as pd

import klass
import tests.mock_request_functions as mock_returns


def test_codes_data_is_dataframe_has_len(
    klass_codes_at_success,
):
    klass_codes = klass_codes_at_success
    assert len(klass_codes.data)
    assert isinstance(klass_codes.data, pd.DataFrame)


@mock.patch("klass.classes.codes.codes_at")
def test_codes_auto_set_from_date(test_codes_at):
    test_codes_at.return_value = mock_returns.codes_at_success()
    codes = klass.KlassCodes(36)
    assert isinstance(codes.from_date, str)
    assert len(codes.from_date)


@mock.patch("klass.classes.codes.codes_at")
def test_codes_change_dates(test_codes_at):
    test_codes_at.return_value = mock_returns.codes_at_success()
    codes = klass.KlassCodes(36)
    codes.change_dates(
        from_date="",
        to_date="",
        include_future=True,
    )
    assert len(codes.from_date)
    assert isinstance(codes.from_date, str)


def test_codes_to_dict(
    klass_codes_at_success,
):
    dict_check = klass_codes_at_success.to_dict()
    default_dict_check = klass_codes_at_success.to_dict(other="other")
    assert dict_check == {"1": "Mann", "2": "Gutt", "3": "Babygutt"}
    assert len(default_dict_check)
    assert default_dict_check["missing_key"] == "other"


def test_codes_to_dict_uses_presentation_name_when_present(
    klass_codes_at_success,
):
    df = klass_codes_at_success.data.copy()
    df["presentationName"] = df["code"] + " - " + df["name"]
    klass_codes_at_success.data = df
    dict_check = klass_codes_at_success.to_dict()
    assert dict_check == {
        "1": "1 - Mann",
        "2": "2 - Gutt",
        "3": "3 - Babygutt",
    }


def test_codes_pivot_level(
    klass_codes_at_success,
):
    df = klass_codes_at_success.pivot_level()
    assert isinstance(df, pd.DataFrame)
    assert len(df)


def test_codes_pivot_level_unordered(klass_codes_at_success):
    klass_codes_at_success.data = klass_codes_at_success.data.sort_values(
        by="level", ascending=False
    )
    df = klass_codes_at_success.pivot_level()
    assert df.isna().sum().sum() == 0


def test_codes_has_str_repr(klass_codes_at_success):
    klass_codes_at_success.from_date = "2023-01-01"
    klass_codes_at_success.language = "en"
    klass_codes_at_success.include_future = True
    assert klass_codes_at_success.__str__()
    assert klass_codes_at_success.__repr__()
    assert len(klass_codes_at_success.__str__())
    assert len(klass_codes_at_success.__repr__())
    print(klass_codes_at_success)
    repr(klass_codes_at_success)
