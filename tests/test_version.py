from unittest import mock

import pandas as pd
import pytest

import tests.mock_request_functions as mock_returns


def test_version_initialization(klass_version_success):
    assert isinstance(klass_version_success.data, pd.DataFrame)
    assert len(klass_version_success.data)


def test_version_has_str_repr(klass_version_success):
    klass_version_success.select_level = 1
    klass_version_success.language = "nn"
    klass_version_success.include_future = True
    assert klass_version_success.__str__()
    assert klass_version_success.__repr__()
    assert len(klass_version_success.__str__())
    assert len(klass_version_success.__repr__())
    print(klass_version_success)
    repr(klass_version_success)


def test_version_simple_correspondences(klass_version_success):
    simple = klass_version_success.correspondences_simple()
    assert len(simple)
    assert isinstance(simple, dict)


@mock.patch("klass.classes.variant.variants_by_id")
def test_version_get_variant_by_search_term_returns_variant(
    mock_variants_by_id, klass_version_success
):
    # Patch the variants endpoint used by KlassVariant
    mock_variants_by_id.return_value = mock_returns.variants_by_id_success()

    # Search term should match the single mocked variant name
    variant = klass_version_success.get_variant(search_term="fagskole")
    assert hasattr(variant, "data") and isinstance(variant.data, pd.DataFrame)
    assert len(variant.data) > 0


def test_version_get_variant_by_search_term_no_match_raises(klass_version_success):
    with pytest.raises(ValueError):
        klass_version_success.get_variant(search_term="no-such-variant")


def test_version_get_variant_missing_identifier_raises(klass_version_success):
    with pytest.raises(ValueError):
        klass_version_success.get_variant()


def test_version_get_variant_non_string_search_term_raises(klass_version_success):
    with pytest.raises(ValueError):
        klass_version_success.get_variant(search_term=123)  # type: ignore[arg-type]
