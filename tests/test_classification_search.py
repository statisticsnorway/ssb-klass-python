def test_classification_search_has_versions_content(
    klass_classification_search_success,
):
    klass_classification_search = klass_classification_search_success
    assert len(klass_classification_search.links)
    assert len(klass_classification_search.classifications)


def test_classification_search_has_str_repr(klass_classification_search_success):
    klass_classification_search_success.ssbsection = "360"
    klass_classification_search_success.include_codelists = True
    klass_classification_search_success.language = "nn"
    assert klass_classification_search_success.__str__()
    assert klass_classification_search_success.__repr__()
    assert len(klass_classification_search_success.__str__())
    assert len(klass_classification_search_success.__repr__())
    print(klass_classification_search_success)
    repr(klass_classification_search_success)


def test_simple_search_result(klass_classification_search_success):
    assert len(klass_classification_search_success.simple_search_result())
    assert isinstance(klass_classification_search_success.simple_search_result(), str)


def test_classification_search_can_be_empty(klass_classification_search_empty):
    assert klass_classification_search_empty.classifications == []
