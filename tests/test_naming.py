"""Thanks chatgippity."""

import pytest

from klass.utility.naming import create_shortname


class NamingObject:
    """Mock class for testing naming-function."""

    def __init__(self, name=None, target=None):
        self.name = name
        self.target = target


@pytest.mark.parametrize(
    "obj,shortname_len,expected",
    [
        (NamingObject(name="example name"), 2, "example_name"),
        (NamingObject(target="custom target"), 2, "custom_target"),
        (NamingObject(name="Hello World Python"), 3, "hello_world_python"),
        (NamingObject(name="Hello World Python"), 2, "hello_world"),
        (NamingObject(name="Hello World Python"), 5, "hello_world_python"),
        (NamingObject(name="æ ø å"), 3, "ae_oe_aa"),
        (NamingObject(name="This&That!More"), 3, "thisthatmore"),
        (NamingObject(name="hyphen-ated words"), 3, "hyphen_ated_words"),
        (NamingObject(name="og apple and banana"), 3, "apple_banana"),
        (
            NamingObject(name="Test! Case? With@ Special# Chars$"),
            3,
            "test_case_with",
        ),
        (NamingObject(name="MixedÆØÅCharacters"), 3, "mixedaeoeaacharacters"),
        (NamingObject(name="Short"), 3, "short"),
    ],
)
def test_create_shortname(obj, shortname_len, expected):
    assert create_shortname(obj, shortname_len) == expected


def test_create_shortname_missing_attribute():
    obj = NamingObject()  # No name or target attribute set
    with pytest.raises(
        ValueError, match=r"Object is missing valid target/name attribute."
    ):
        create_shortname(obj)
