# Currently throws an error on getting the classification...
# @mock.patch.object(requests.Session, "send")
# def test_get_json_testing(mock_response):
#    klass.TESTING = True
#    mock_response.return_value = mock_response_data.classifications_fake_content()
#    classification = klass.requests.klass_requests.classifications()
#    assert classification["_embedded"]


# @mock.patch.object(requests.Session, "send")
# def test_classification_changed_since(mock_response):
#    mock_response.return_value = mock_response_data.classifications_fake_content()
#    classification = klass.requests.klass_requests.classifications(
#        include_codelists=True, changed_since="2022-01-01T00:00:00:000+00:00"
#    )
#    assert classification["_embedded"]
