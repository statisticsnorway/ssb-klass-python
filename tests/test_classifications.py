def test_classification_has_versions_content(klass_classification_success):
    klass_classification = klass_classification_success
    assert len(klass_classification.versions)
    assert len(klass_classification.versions[0])
