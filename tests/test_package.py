import klass


def test_getting_version_from_pyproject():
    klass._try_getting_pyproject_toml()
    version = klass.__version__
    assert version.replace(".", "").isnumeric()
    assert int(version.replace(".", "")) > 0
