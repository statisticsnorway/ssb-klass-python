import pandas as pd


def test_version_initialization(klass_version_success):
    assert isinstance(klass_version_success.data, pd.DataFrame)
    assert len(klass_version_success.data)


def test_version_has_str_repr(klass_version_success):
    klass_version_success.select_level = 1
    klass_version_success.language = "nn"
    klass_version_success.include_future = True
    assert klass_version_success.__str__()
    assert klass_version_success.__repr__()
    assert len(klass_version_success.__str__())
    assert len(klass_version_success.__repr__())
    print(klass_version_success)
    repr(klass_version_success)


def test_version_simple_correspondences(klass_version_success):
    simple = klass_version_success.correspondences_simple()
    assert len(simple)
    assert isinstance(simple, dict)
