import klass


def test_ClassificationSearchType_has_versions_content(
    klass_classification_search_success,
):
    klass_classification_search = klass_classification_search_success
    assert len(klass_classification_search.links)
    assert len(klass_classification_search.classifications)


def test_ClassificationSearchType_has_str_repr(klass_classification_search_success):
    assert klass_classification_search_success.__str__()
    assert klass_classification_search_success.__repr__()
    assert len(klass_classification_search_success.__str__())
    assert len(klass_classification_search_success.__repr__())


def test_gui_formatting(klass_classification_search_success):
    result = klass.widgets.search_ipywidget.format_classification_text(
        klass_classification_search_success
    )
    assert len(result)
    assert isinstance(result, str)
