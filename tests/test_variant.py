def test_variant_classificationitems_has_expected_content(
    klass_variant_success,
):
    items = klass_variant_success.classificationItems
    assert len(items)
    assert isinstance(items, list)
    assert isinstance(items[0], dict)
    assert len(items[0])


def test_variant_has_str_repr(klass_variant_success):
    klass_variant_success.to_date = "2023-01-01"
    klass_variant_success.select_codes = "1"
    klass_variant_success.select_level = "1"
    klass_variant_success.presentation_name_pattern = r"{name} - {code}"
    klass_variant_success.language = "nn"
    klass_variant_success.include_future = True
    assert klass_variant_success.__str__()
    assert klass_variant_success.__repr__()
    assert len(klass_variant_success.__str__())
    assert len(klass_variant_success.__repr__())
    print(klass_variant_success)
    repr(klass_variant_success)
