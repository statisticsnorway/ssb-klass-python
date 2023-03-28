import requests
from functools import lru_cache
from load_config import BASE_URL

# As these functions are used by the validate functions also,
# they are in their own file to avoid circular imports


@lru_cache(maxsize=1)
def sections_list() -> list:
    url = BASE_URL + '/ssbsections'
    response = requests.get(url).json()
    sections = [x["name"] for x in response["_embedded"]["ssbSections"]]
    return sections


def sections_dict() -> dict:
    return {s.split(" ")[0]: s for s in sections_list()}
