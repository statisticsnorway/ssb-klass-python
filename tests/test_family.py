def test_family_initialized(klass_search_families_by_id_success):
    assert len(klass_search_families_by_id_success.families)


def test_search_families_by_id_has_str_repr(klass_search_families_by_id_success):
    klass_search_families_by_id_success.ssbsection = "360"
    klass_search_families_by_id_success.include_codelists = True
    klass_search_families_by_id_success.language = "nn"
    assert klass_search_families_by_id_success.__str__()
    assert klass_search_families_by_id_success.__repr__()
    assert len(klass_search_families_by_id_success.__str__())
    assert len(klass_search_families_by_id_success.__repr__())
    print(klass_search_families_by_id_success)
    repr(klass_search_families_by_id_success)


def test_search_families_simple_search_result(klass_search_families_by_id_success):
    assert len(klass_search_families_by_id_success.simple_search_result())
    assert isinstance(klass_search_families_by_id_success.simple_search_result(), str)
