from unittest import mock

import pytest

import klass
import tests.mock_request_functions as mock_returns


@pytest.fixture
@mock.patch("klass.classes.classification.classification_by_id")
@mock.patch("klass.classes.classification.changes")
def klass_classification_success(test_changes, test_classification_by_id):
    test_changes.return_value = mock_returns.changes_success()
    test_classification_by_id.return_value = mock_returns.classification_by_id_success()
    return klass.KlassClassification("0")


@pytest.fixture
@mock.patch("klass.classes.search.classification_search")
def klass_classification_search_success(test_classification_search):
    test_classification_search.return_value = (
        mock_returns.classification_search_success()
    )
    return klass.KlassSearchClassifications("Nus")


@pytest.fixture
@mock.patch("klass.classes.codes.codes_at")
def klass_codes_at_success(test_codes_at):
    test_codes_at.return_value = mock_returns.codes_at_success()
    return klass.KlassCodes(36)


@pytest.fixture
@mock.patch("klass.classes.variant.variants_by_id")
def klass_variant_success(test_variants_by_id):
    test_variants_by_id.return_value = mock_returns.variants_by_id_success()
    return klass.KlassVariant(36)


@pytest.fixture
@mock.patch("klass.classes.variant.variant_at")
@mock.patch("klass.classes.variant.variant")
def klass_variants_search_success(test_variant, test_variant_at):
    test_variant.return_value = mock_returns.variant_success()
    test_variant_at.return_value = mock_returns.variant_at_success()
    return klass.KlassVariantsSearch("0", "Variant name")


@pytest.fixture
@mock.patch("klass.classes.correspondance.correspondance_table_by_id")
@mock.patch("klass.classes.correspondance.corresponds")
def klass_correspondance_success(test_corresponds, test_correspondance_table_by_id):
    test_corresponds.return_value = mock_returns.corresponds_success()
    test_correspondance_table_by_id.return_value = (
        mock_returns.correspondance_table_by_id_success()
    )
    # Fail on not working sending in just source and target
    klass.klass.KlassCorrespondance(
        source_classification_id="0", target_classification_id="1"
    )
    return klass.KlassCorrespondance(correspondance_id="0")
