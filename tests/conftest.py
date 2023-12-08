from unittest import mock

import pytest

import klass
import tests.mock_request_functions as mock_returns


@pytest.fixture
@mock.patch("klass.classes.classification.classification_by_id")
@mock.patch.object(klass.KlassClassification, "get_changes")
def klass_classification_success(test_changes, tesClassificationsByIdType):
    test_changes.return_value = mock_returns.changes_success()
    tesClassificationsByIdType.return_value = (
        mock_returns.classification_by_id_success()
    )
    result = klass.KlassClassification("0", language="en", include_future=True)
    # Why do I have to hack it like this :( IM SORRY OK
    result.get_changes = test_changes
    return result


@pytest.fixture
@mock.patch("klass.classes.search.classification_search")
def klass_classification_search_success(tesClassificationSearchType):
    tesClassificationSearchType.return_value = (
        mock_returns.classification_search_success()
    )
    return klass.KlassSearchClassifications("Nus")


@pytest.fixture
@mock.patch("klass.classes.codes.codes_at")
def klass_codes_at_success(test_codes_at):
    test_codes_at.return_value = mock_returns.codes_at_success()
    return klass.KlassCodes(
        36,
        from_date="2023-01-01",
        to_date="2023-09-30",
        select_codes="1",
        select_level="1",
        presentation_name_pattern=r"{code} - {name}",
        language="en",
        include_future=True,
    )


@pytest.fixture
@mock.patch("klass.classes.variant.variants_by_id")
def klass_variant_success(tesVariantsByIdType):
    tesVariantsByIdType.return_value = mock_returns.variants_by_id_success()
    return klass.KlassVariant(36)


@pytest.fixture
@mock.patch("klass.classes.variant.variant_at")
@mock.patch("klass.classes.variant.variant")
def klass_variant_search_success(test_variant, test_variant_at):
    test_variant.return_value = mock_returns.variant_success()
    test_variant_at.return_value = mock_returns.variant_at_success()
    return klass.KlassVariantSearchByName("0", "Variant name", "2023-01-01")


@pytest.fixture
@mock.patch("klass.classes.correspondence.correspondence_table_by_id")
@mock.patch("klass.classes.correspondence.corresponds")
def klass_correspondence_from_id_success(
    tescorrespondstype, test_correspondence_table_by_id
):
    tescorrespondstype.return_value = mock_returns.corresponds_success()
    test_correspondence_table_by_id.return_value = (
        mock_returns.correspondence_table_by_id_success()
    )
    return klass.KlassCorrespondence(correspondence_id="0")


@pytest.fixture
@mock.patch("klass.classes.correspondence.correspondence_table_by_id")
@mock.patch("klass.classes.correspondence.corresponds")
def klass_correspondence_between_classifications_success(
    test_correspondstype, test_correspondence_table_by_id
):
    test_correspondstype.return_value = mock_returns.corresponds_success()
    test_correspondence_table_by_id.return_value = (
        mock_returns.correspondence_table_by_id_success()
    )
    # Fail on not working sending in just source and target
    return klass.KlassCorrespondence(
        source_classification_id="0",
        target_classification_id="1",
        from_date="2023-01-01",
    )


@pytest.fixture
@mock.patch("klass.classes.family.classificationfamilies_by_id")
def klass_search_families_by_id_success(
    test_classificationfamilies_by_id,
):
    test_classificationfamilies_by_id.return_value = (
        mock_returns.classificationfamilies_by_id_success()
    )
    return klass.KlassSearchFamilies("320")
