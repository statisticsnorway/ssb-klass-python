from unittest import mock

import pytest

import klass
from tests.mock_request_functions import (
    classification_by_id_success,
    classification_search_success,
)


@pytest.fixture
@mock.patch("klass.classes.classification.classification_by_id")
def klass_classification_success(test_classification_by_id):
    test_classification_by_id.return_value = classification_by_id_success()
    return klass.KlassClassification("0")


@pytest.fixture
@mock.patch("klass.classes.search.classification_search")
def klass_classification_search_success(test_classification_search):
    test_classification_search.return_value = classification_search_success()
    return klass.KlassSearchClassification("Nus")
