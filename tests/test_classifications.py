from unittest import mock

import pandas as pd

import klass


def test_classification_has_versions_content(klass_classification_success):
    klass_classification = klass_classification_success
    assert len(klass_classification.versions)
    assert len(klass_classification.versions[0])


def test_classification_can_get_changes(klass_classification_success):
    changes = klass_classification_success.get_changes("2020-01-01")
    assert isinstance(changes, pd.DataFrame)
    assert len(changes)


def test_classification_has_str_repr(klass_classification_success):
    klass_classification_success.language = "en"
    klass_classification_success.include_future = True
    assert klass_classification_success.__str__()
    assert klass_classification_success.__repr__()
    assert len(klass_classification_success.__str__())
    assert len(klass_classification_success.__repr__())
    print(klass_classification_success)
    repr(klass_classification_success)


def test_version_dict(klass_classification_success):
    assert len(klass_classification_success.versions_dict())


# @mock.patch("klass.classes.classification.get_version")
@mock.patch.object(klass.KlassClassification, "get_version")
def test_get_version_from_classification(
    mock_get_version, klass_classification_success, klass_version_success
):
    mock_get_version.return_value = klass_version_success
    version = klass_classification_success.get_version()
    assert isinstance(version, klass.KlassVersion)
    assert isinstance(version.data, pd.DataFrame)
    assert len(version.data)


@mock.patch("klass.KlassVariant")
@mock.patch.object(klass.KlassClassification, "get_version")
def test_get_variant_with_only_search_string(
    mock_get_version,
    klassvariant_mock,
    klass_classification_success,
    klass_version_success,
    klass_variant_success,
):
    mock_get_version.return_value = klass_version_success
    klassvariant_mock.return_value = klass_variant_success
    variant = klass_classification_success.get_latest_variant_by_name("fagskole")
    assert isinstance(variant.data, pd.DataFrame)
    assert len(variant.data) > 0
