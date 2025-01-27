import pandas as pd


def test_variant_has_versions_content(
    klass_variant_search_success,
):
    version_data = klass_variant_search_success.data
    assert len(version_data)
    assert isinstance(version_data, pd.DataFrame)


def test_variant_has_str_repr(klass_variant_search_success):
    assert klass_variant_search_success.__str__()
    assert klass_variant_search_success.__repr__()
    assert len(klass_variant_search_success.__str__())
    assert len(klass_variant_search_success.__repr__())
    print(klass_variant_search_success)
    repr(klass_variant_search_success)


def test_variant_to_dict(klass_variant_search_success):
    dict_check = klass_variant_search_success.to_dict()
    default_dict_check = klass_variant_search_success.to_dict(other="other")
    assert len(dict_check)
    assert len(default_dict_check)
    assert default_dict_check["missing_key"] == "other"
