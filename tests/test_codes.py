import pandas as pd


def test_codes_data_is_dataframe_has_len(
    klass_codes_at_success,
):
    klass_codes = klass_codes_at_success
    assert len(klass_codes.data)
    assert isinstance(klass_codes.data, pd.DataFrame)


def test_codes_has_str_repr(klass_codes_at_success):
    assert klass_codes_at_success.__str__()
    assert klass_codes_at_success.__repr__()
    assert len(klass_codes_at_success.__str__())
    assert len(klass_codes_at_success.__repr__())
