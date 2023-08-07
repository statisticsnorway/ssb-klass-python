import pandas as pd


def test_classification_has_versions_content(klass_classification_success):
    klass_classification = klass_classification_success
    assert len(klass_classification.versions)
    assert len(klass_classification.versions[0])


def test_classification_can_get_changes(klass_classification_success):
    changes = klass_classification_success.get_changes("2020-01-01")
    assert isinstance(changes, pd.DataFrame)
    assert len(changes)
