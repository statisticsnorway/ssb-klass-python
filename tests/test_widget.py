from unittest import mock

import klass


@mock.patch("klass.classes.search.KlassSearchClassifications")
def test_gui_display(klass_classification_search_success):
    klass_classification_search_success.return_value = (
        klass_classification_search_success()
    )
    klass.widgets.search_ipywidget.search_classification()


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
