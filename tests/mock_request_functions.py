from unittest import mock

import requests

from klass.requests import klass_requests
from klass.requests import sections
from tests import mock_response_data


@mock.patch.object(requests.Session, "send")
def classifications_success(mock_response):
    mock_response.return_value = mock_response_data.classifications_fake_content()
    return klass_requests.classifications()


@mock.patch.object(requests.Session, "send")
def classification_by_id_success(mock_response):
    mock_response.return_value = mock_response_data.classification_by_id_fake_content()
    return klass_requests.classification_by_id("0")


@mock.patch.object(requests.Session, "send")
def classification_search_success(mock_response):
    mock_response.return_value = mock_response_data.classification_search_fake_content()
    return klass_requests.classification_search("Nus")


@mock.patch.object(requests.Session, "send")
def codes_at_success(mock_response):
    mock_response.return_value = mock_response_data.codes_at_fake_content()
    return klass_requests.codes_at("0", date="2023-01-01")


@mock.patch.object(requests.Session, "send")
def version_by_id_success(mock_response):
    mock_response.return_value = mock_response_data.version_by_id_fake_content()
    return klass_requests.version_by_id("0")


@mock.patch.object(requests.Session, "send")
def variant_success(mock_response):
    mock_response.return_value = mock_response_data.variant_fake_content()
    return klass_requests.variant("0", "Variant name", "2023-01-01")


@mock.patch.object(requests.Session, "send")
def variant_at_success(mock_response):
    mock_response.return_value = mock_response_data.variant_at_fake_content()
    return klass_requests.variant_at("0", "Variant name", "2023-01-01")


@mock.patch.object(requests.Session, "send")
def variants_by_id_success(mock_response):
    mock_response.return_value = mock_response_data.variants_by_id_fake_content()
    return klass_requests.variants_by_id("0")


@mock.patch.object(requests.Session, "send")
def corresponds_success(mock_response):
    mock_response.return_value = mock_response_data.corresponds_fake_content()
    return klass_requests.corresponds("0", "1", "2023-01-01")


@mock.patch.object(requests.Session, "send")
def corresponds_at_success(mock_response):
    mock_response.return_value = mock_response_data.corresponds_at_fake_content()
    return klass_requests.corresponds_at("0", "1", "2023-01-01")


@mock.patch.object(requests.Session, "send")
def correspondence_table_by_id_success(mock_response):
    mock_response.return_value = (
        mock_response_data.correspondence_table_by_id_fake_content()
    )
    return klass_requests.correspondence_table_by_id("0")


@mock.patch.object(requests.Session, "send")
def changes_success(mock_response):
    mock_response.return_value = mock_response_data.changes_fake_content()
    return klass_requests.changes("0", "2023-01-01")


@mock.patch.object(requests.Session, "send")
def classificationfamilies_success(mock_response):
    mock_response.return_value = (
        mock_response_data.classificationfamilies_fake_content()
    )
    return klass_requests.classificationfamilies("360")


@mock.patch.object(requests.Session, "send")
def classificationfamilies_by_id_success(mock_response):
    mock_response.return_value = (
        mock_response_data.classificationfamilies_by_id_fake_content()
    )
    return klass_requests.classificationfamilies_by_id("20")


@mock.patch.object(requests.Session, "send")
def sections_list_success(mock_response):
    mock_response.return_value = mock_response_data.sections_fake_content()
    return sections.sections_list()
