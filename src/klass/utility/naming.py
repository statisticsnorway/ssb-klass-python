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
    parts = name.split(" ")
    if len(parts) < shortname_len:
        shortname_len = len(parts)
    return "_".join(parts[:shortname_len]).lower()