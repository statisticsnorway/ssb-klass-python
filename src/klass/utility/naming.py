from typing import Any


def create_shortname(elem: Any, shortname_len: int = 3) -> str:
    """Create a column name from an object that has a target or name attribute.

    Args:
        elem: The object that has the target/name attribute.
        shortname_len: The amount of elements from the name attribute to use in the shortname.

    Returns:
        str: A constructed column name containing no spaces.

    Raises:
        ValueError: If the object is missing a name attribute.
    """
    if hasattr(elem, "target"):
        name = elem.target
    elif not hasattr(elem, "name"):
        raise ValueError("Object is missing target/name attribute.")
    else:
        name = elem.name
    replace = {
        k: ""
        for k in [
            chr(i) for i in range(33, 127) if not chr(i).isalnum() and chr(i) != "-"
        ]
    } | {
        "og ": "",
        "and ": "",
        "Æ": "Ae",
        "Ø": "Oe",
        "Å": "Aa",
        "æ": "ae",
        "ø": "oe",
        "å": "aa",
        "-": "_",  # Overloads the one coming from the first dict
    }
    for k, v in replace.items():
        name = name.replace(k, v)

    parts = name.split(" ")
    if len(parts) < shortname_len:
        shortname_len = len(parts)
    return "_".join(parts[:shortname_len]).lower()
