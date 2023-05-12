import pytest
from unittest import mock
import requests
from klass import KlassClassification
from klass.requests import klass_requests
import mock_responses


@mock.patch.object(requests.Session, "send")
def classifications_success(mock_response):
    mock_response.return_value = mock_responses.classifications_fake_content()
    return klass_requests.classifications()


@mock.patch.object(requests.Session, "send")
def classification_by_id_success(mock_response):
    mock_response.return_value = mock_responses.classification_by_id_fake_content()
    return klass_requests.classification_by_id("0")


@pytest.fixture
@mock.patch("klass.classes.classification.classification_by_id")
def KlassClassification_success(test_classification_by_id):
    test_classification_by_id.return_value = classification_by_id_success()
    return KlassClassification("0")


def test_classification_has_versions_content(KlassClassification_success):
    klass_classification = KlassClassification_success
    assert len(klass_classification.versions)
    assert len(klass_classification.versions[0])