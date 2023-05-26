from unittest import mock

import requests

from klass.requests import klass_requests
from tests import mock_response_data


@mock.patch.object(requests.Session, "send")
def classifications_success(mock_response):
    mock_response.return_value = mock_response_data.classifications_fake_content()
    return klass_requests.classifications()


@mock.patch.object(requests.Session, "send")
def classification_by_id_success(mock_response):
    mock_response.return_value = mock_response_data.classification_by_id_fake_content()
    return klass_requests.classification_by_id("0")
