def test_variant_classificationitems_has_expected_content(
    klass_variant_success,
):
    items = klass_variant_success.classificationItems
    assert len(items)
    assert isinstance(items, list)
    assert isinstance(items[0], dict)
    assert len(items[0])
