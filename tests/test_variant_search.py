import pandas as pd


def test_classification_search_has_versions_content(
    klass_variant_search_success,
):
    version_data = klass_variant_search_success.data
    assert len(version_data)
    assert isinstance(version_data, pd.DataFrame)
