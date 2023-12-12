from unittest import mock

import pandas as pd
import requests

import klass
import tests


@mock.patch.object(requests.Session, "send")
def test_get_json_testing(mock_response):
    klass.config.TESTING = True
    mock_response.return_value = tests.mock_response_data.classifications_fake_content()
    classification = klass.requests.klass_requests.classifications()
    assert len(classification["_embedded"])


@mock.patch.object(requests.Session, "send")
def test_classification_changed_since(mock_response):
    mock_response.return_value = tests.mock_response_data.classifications_fake_content()
    classification = klass.requests.klass_requests.classifications(
        include_codelists=True, changed_since="2022-01-01T00:00:00:000+00:00"
    )
    assert classification["_embedded"]


@mock.patch.object(requests, "get")
@mock.patch.object(requests.Session, "send")
def test_classification_search(mock_response, sections_list):
    sections_list.return_value = tests.mock_response_data.sections_fake_content()
    mock_response.return_value = (
        tests.mock_response_data.classification_search_fake_content()
    )
    query = "test query"
    include_codelists = True
    ssbsection = "360"
    result = klass.requests.klass_requests.classification_search(
        query=query, include_codelists=include_codelists, ssbsection=ssbsection
    )
    assert len(result["page"])


@mock.patch.object(requests.Session, "send")
def test_classification_by_id(mock_response):
    mock_response.return_value = (
        tests.mock_response_data.classification_by_id_fake_content()
    )
    classification_id = "36"
    language = "nn"
    include_future = True
    result = klass.requests.klass_requests.classification_by_id(
        classification_id=classification_id,
        language=language,
        include_future=include_future,
    )
    assert len(result["versions"])


@mock.patch.object(requests.Session, "send")
def test_codes(mock_response):
    mock_response.return_value = tests.mock_response_data.codes_fake_content()

    # Test parameters
    classification_id = "36"
    from_date = "2022-01-01"
    to_date = "2022-12-31"
    select_codes = "1"
    select_level = "1"
    presentation_name_pattern = "{name} - {code}"
    language = "nn"
    include_future = True

    # Call the request function
    result = klass.requests.klass_requests.codes(
        classification_id=classification_id,
        from_date=from_date,
        to_date=to_date,
        select_codes=select_codes,
        select_level=select_level,
        presentation_name_pattern=presentation_name_pattern,
        language=language,
        include_future=include_future,
    )

    # Assert the result
    assert len(result["validFrom"])
    # Add more specific assertions based on the response structure or expected values as needed


@mock.patch.object(requests.Session, "send")
def test_codes_at(mock_response):
    mock_response.return_value = tests.mock_response_data.codes_at_fake_content()

    # Test parameters
    classification_id = "36"
    date = "2022-01-01"
    select_codes = "1"
    select_level = "1"
    presentation_name_pattern = "{name} - {code}"
    language = "nn"
    include_future = True

    # Call the request function
    result = klass.requests.klass_requests.codes_at(
        classification_id=classification_id,
        date=date,
        select_codes=select_codes,
        select_level=select_level,
        presentation_name_pattern=presentation_name_pattern,
        language=language,
        include_future=include_future,
    )

    # Assert the result
    assert len(result["validFrom"])


@mock.patch.object(requests.Session, "send")
def test_version_by_id(mock_response):
    mock_response.return_value = tests.mock_response_data.version_by_id_fake_content()

    # Test parameters
    version_id = "1576"
    language = "nn"
    include_future = True

    # Call the request function
    result = klass.requests.klass_requests.version_by_id(
        version_id=version_id, language=language, include_future=include_future
    )

    # Assert the result
    assert len(result["correspondenceTables"])


@mock.patch.object(requests.Session, "send")
def test_variant(mock_response):
    mock_response.return_value = tests.mock_response_data.variant_fake_content()

    # Test parameters
    classification_id = "36"
    variant_name = "Variant name"
    from_date = "2022-01-01"
    to_date = "2022-12-31"
    select_codes = "1"
    select_level = "1"
    presentation_name_pattern = "{name} - {code}"
    language = "nn"
    include_future = True

    # Call the request function
    result = klass.requests.klass_requests.variant(
        classification_id=classification_id,
        variant_name=variant_name,
        from_date=from_date,
        to_date=to_date,
        select_codes=select_codes,
        select_level=select_level,
        presentation_name_pattern=presentation_name_pattern,
        language=language,
        include_future=include_future,
    )

    assert isinstance(result, pd.DataFrame)
    assert len(result)


@mock.patch.object(requests.Session, "send")
def test_variant_at(mock_response):
    mock_response.return_value = tests.mock_response_data.variant_at_fake_content()

    # Test parameters
    classification_id = "36"
    variant_name = "Variant name"
    date = "2022-01-01"
    select_codes = "1"
    select_level = "1"
    presentation_name_pattern = "{name} - {code}"
    language = "nn"
    include_future = True

    # Call the request function
    result = klass.requests.klass_requests.variant_at(
        classification_id=classification_id,
        variant_name=variant_name,
        date=date,
        select_codes=select_codes,
        select_level=select_level,
        presentation_name_pattern=presentation_name_pattern,
        language=language,
        include_future=include_future,
    )

    assert isinstance(result, pd.DataFrame)
    assert len(result)


@mock.patch.object(requests.Session, "send")
def test_variants_by_id(mock_response):
    mock_response.return_value = tests.mock_response_data.variants_by_id_fake_content()

    # Test parameters
    variant_id = "1567"
    language = "en"

    # Call the request function
    result = klass.requests.klass_requests.variants_by_id(
        variant_id=variant_id, language=language
    )

    # Assert the result
    assert len(result["classificationItems"])


@mock.patch.object(requests.Session, "send")
def test_corresponds(mock_response):
    mock_response.return_value = tests.mock_response_data.corresponds_fake_content()

    # Test parameters
    source_classification_id = "136"
    target_classification_id = "146"
    from_date = "2022-01-01"
    to_date = "2022-12-31"
    language = "en"
    include_future = True

    # Call the request function
    result = klass.requests.klass_requests.corresponds(
        source_classification_id=source_classification_id,
        target_classification_id=target_classification_id,
        from_date=from_date,
        to_date=to_date,
        language=language,
        include_future=include_future,
    )

    # Assert the result
    assert len(result["correspondenceItems"])


@mock.patch.object(requests.Session, "send")
def test_corresponds_at(mock_response):
    mock_response.return_value = tests.mock_response_data.corresponds_at_fake_content()

    # Test parameters
    source_classification_id = "136"
    target_classification_id = "146"
    date = "2022-01-01"
    language = "en"
    include_future = True

    # Call the request function
    result = klass.requests.klass_requests.corresponds_at(
        source_classification_id=source_classification_id,
        target_classification_id=target_classification_id,
        date=date,
        language=language,
        include_future=include_future,
    )

    # Assert the result
    assert len(result["correspondenceItems"])


@mock.patch.object(requests.Session, "send")
def test_correspondence_table_by_id(mock_response):
    mock_response.return_value = (
        tests.mock_response_data.correspondence_table_by_id_fake_content()
    )

    # Test parameters
    correspondence_id = "1765"
    language = "en"

    # Call the request function
    result = klass.requests.klass_requests.correspondence_table_by_id(
        correspondence_id=correspondence_id, language=language
    )

    # Assert the result
    assert len(result["correspondenceMaps"])


@mock.patch.object(requests.Session, "send")
def test_changes(mock_response):
    mock_response.return_value = tests.mock_response_data.changes_fake_content()

    # Test parameters
    classification_id = "1567"
    from_date = "2022-01-01"
    to_date = "2022-12-31"
    language = "en"
    include_future = True

    # Call the request function
    result = klass.requests.klass_requests.changes(
        classification_id=classification_id,
        from_date=from_date,
        to_date=to_date,
        language=language,
        include_future=include_future,
    )

    # Assert the result
    assert isinstance(result, pd.DataFrame)
    assert len(result)


@mock.patch.object(requests.Session, "send")
def test_classificationfamilies(mock_response):
    mock_response.return_value = (
        tests.mock_response_data.classificationfamilies_fake_content()
    )

    # Test parameters
    ssbsection = "360"
    include_codelists = True
    language = "en"

    # Call the request function
    result = klass.requests.klass_requests.classificationfamilies(
        ssbsection=ssbsection, include_codelists=include_codelists, language=language
    )

    # Assert the result
    assert len(result["_embedded"])


@mock.patch.object(requests.Session, "send")
def test_classificationfamilies_by_id(mock_response):
    mock_response.return_value = (
        tests.mock_response_data.classificationfamilies_by_id_fake_content()
    )

    # Test parameters
    classificationfamily_id = "1576"
    ssbsection = "360"
    include_codelists = True
    language = "en"

    # Call the request function
    result = klass.requests.klass_requests.classificationfamilies_by_id(
        classificationfamily_id=classificationfamily_id,
        ssbsection=ssbsection,
        include_codelists=include_codelists,
        language=language,
    )

    # Assert the result
    assert len(result["classifications"])
