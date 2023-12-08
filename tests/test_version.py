import pandas as pd


def test_version_initialization(klass_version_success):
    assert isinstance(klass_version_success.data, pd.DataFrame)
    assert len(klass_version_success.data)


def test_version_has_str_repr(klass_version_success):
    assert klass_version_success.__str__()
    assert klass_version_success.__repr__()
    assert len(klass_version_success.__str__())
    assert len(klass_version_success.__repr__())


def test_version_simple_correspondences(klass_version_success):
    simple = klass_version_success.correspondences_simple()
    assert len(simple)
    assert isinstance(simple, dict)
