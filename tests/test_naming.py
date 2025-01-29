"""Thanks chatgippity."""

import pytest

from klass.utility.naming import create_shortname


class TestNamingObject:
    def __init__(self, name=None, target=None):
        self.name = name
        self.target = target


@pytest.mark.parametrize(
    "obj,shortname_len,expected",
    [
        (TestNamingObject(name="example name"), 2, "example_name"),
        (TestNamingObject(target="custom target"), 2, "custom_target"),
        (TestNamingObject(name="Hello World Python"), 3, "hello_world_python"),
        (TestNamingObject(name="Hello World Python"), 2, "hello_world"),
        (TestNamingObject(name="Hello World Python"), 5, "hello_world_python"),
        (TestNamingObject(name="æ ø å"), 3, "ae_oe_aa"),
        (TestNamingObject(name="This&That!More"), 3, "thisthatmore"),
        (TestNamingObject(name="hyphen-ated words"), 3, "hyphen_ated_words"),
        (TestNamingObject(name="og apple and banana"), 3, "apple_banana"),
        (TestNamingObject(name="Test! Case? With@ Special# Chars$"), 3, "test_case_with"),
        (TestNamingObject(name="MixedÆØÅCharacters"), 3, "mixedaeoeaacharacters"),
        (TestNamingObject(name="Short"), 3, "short"),
    ],
)
def test_create_shortname(obj, shortname_len, expected):
    assert create_shortname(obj, shortname_len) == expected


def test_create_shortname_missing_attribute():
    obj = TestNamingObject()  # No name or target attribute set
    with pytest.raises(ValueError, match="Object is missing valid target/name attribute."):
        create_shortname(obj)
