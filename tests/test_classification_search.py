def test_classification_search_has_versions_content(
    klass_classification_search_success,
):
    klass_classification_search = klass_classification_search_success
    assert len(klass_classification_search.links)
    assert len(klass_classification_search.classifications)
