from unittest import mock

import pytest

from klass import KlassClassification
from tests.mock_request_functions import classification_by_id_success


@pytest.fixture
@mock.patch("klass.classes.classification.classification_by_id")
def klass_classification_success(test_classification_by_id):
    test_classification_by_id.return_value = classification_by_id_success()
    return KlassClassification("0")
