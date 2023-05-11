from functools import lru_cache
from ..klass_config import KlassConfig


# As these functions are used by the validate functions also,
# they are in their own file to avoid circular imports


@lru_cache(maxsize=1)
def sections_list() -> list:
    url = KlassConfig().BASE_URL + '/ssbsections'
    response = requests.get(url).json()
    sections = [x["name"] for x in response["_embedded"]["ssbSections"]]
    return sections


def sections_dict() -> dict:
    return {s.split(" ")[0]: s for s in sections_list()}
