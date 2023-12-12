from unittest import mock

import klass


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


def test_gui_formatting(klass_classification_search_success):
    result = klass.widgets.search_ipywidget.format_classification_text(
        klass_classification_search_success
    )
    assert len(result)
    assert isinstance(result, str)


def test_gui_formatting_empty_result(klass_classification_search_empty):
    result = klass.widgets.search_ipywidget.format_classification_text(
        klass_classification_search_empty
    )
    assert "no matching" in result.lower()
    assert isinstance(result, str)


@mock.patch("klass.classes.search.KlassSearchClassifications")
def test_gui_display(klass_classification_search_success):
    klass_classification_search_success.return_value = (
        klass_classification_search_success()
    )
    klass.widgets.search_ipywidget.search_classification()


def test_classification_search_can_be_empty(klass_classification_search_empty):
    assert klass_classification_search_empty.classifications == []
