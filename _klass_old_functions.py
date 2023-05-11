import json
from datetime import datetime

import pandas as pd
import requests
import toml


config = toml.loads("config.toml")
BASE_URL = config["BASE_URL"]


def klass_get(url: str, level: str = ""):
    """
    Parameter1: URL, the uri to a KLASS-API endpoint. Like
    https://data.ssb.no/api/klass/v1/classifications/533/codes.json?from=2020-01-01&includeFuture=True
    Parameter2: Level, defined by the API, like "codes"
    Parameter3: return_df, returns json if set to False, a pandas dataframe if True
    Returns: a pandas dataframe with the classification
    """
    if url[:8] != "https://":
        raise requests.HTTPError("Please use https, not http.")
    r = requests.get(url)
    # HTTP-errorcode handling
    if r.status_code != 200:
        raise requests.HTTPError(
            f"Connection error: {r.status_code}. Try using https on Dapla?"
        )
    # Continue munging result
    response = json.loads(r.text)
    if level:
        response = response[level]
    return response


def klass_df(url: str, level: str = ""):
    """
    By using this function to imply that you want a dataframe back.
    Parameter1: URL, the uri to a KLASS-API endpoint. Like
    https://data.ssb.no/api/klass/v1/classifications/533/codes.json?from=2020-01-01&includeFuture=True
    Parameter2: Level, defined by the API, like "codes"
    Returns: a pandas dataframe with the classification
    """
    return pd.json_normalize(klass_get(url, level))


def variant_df(variant_id: int, language="nb") -> pd.DataFrame:
    url = BASE_URL + "variants/" + str(variant_id) + "?language=" + language
    print(url)
    return klass_df(url, level="classificationItems")


def classification_codes_df(
    classification_id: int,
    from_date: str = "",
    to_date: str = "",
    include_future: bool = True,
) -> pd.DataFrame:
    url = BASE_URL + "classifications/" + str(classification_id) + "/codes.json?"
    url_params = []
    if from_date:
        url_params += [f"from={validate_date(from_date)}"]
    if to_date:
        url_params += [f"from={validate_date(to_date)}"]
    if include_future:
        url_params += ["includeFuture=True"]
    url += "&".join(url_params)
    print(url)
    return klass_df(url, level="codes")


def correspondance_codes_dict(corr_id: str) -> dict:
    """Get a correspondance from its ID and
    return a dict of the correspondanceMaps["sourceCode"] as keys
    to the correspondanceMaps["targetCode"] as values.
    Apply this to a column in pandas with the .map method for example."""
    if isinstance(corr_id, float):
        corr_id = int(corr_id)
    if isinstance(corr_id, int):
        corr_id = str(corr_id)
    url = BASE_URL + "correspondencetables/" + corr_id
    corr = klass_get(url, "correspondenceMaps")
    return dict(zip([x["sourceCode"] for x in corr], [x["targetCode"] for x in corr]))


def search_classifications(
    searchterm: str, page: int = 0, size: int = 20, ssb_section: int = 0
) -> list:
    url = (
        BASE_URL
        + "classifications/search?query="
        + searchterm
        + "&page="
        + str(page)
        + "&size="
        + str(size)
    )
    if ssb_section:
        url += f"&ssbsection={ssb_section_longname(ssb_section).replace(' ', '%20')}"
    print(url)
    search_result = klass_get(url, "_embedded")
    for result in search_result["searchResults"]:
        print(result["name"], result["_links"]["self"]["href"])


def find_changes(classification_id: int, from_date: str, to_date: str) -> list:
    url = (
        BASE_URL
        + "classifications/"
        + str(classification_id)
        + "/changes.json?from="
        + validate_date(from_date)
        + "&to="
        + validate_date(to_date)
    )
    print(url)
    return klass_df(url, level="codeChanges")


def ssb_section_longname(num: int) -> str:
    for longname in ssb_sections():
        if longname.startswith(str(num)):
            return longname
    return num


def ssb_sections() -> list:
    search_result = klass_get(BASE_URL + "ssbsections", "_embedded")
    return [x["name"] for x in search_result["ssb_sections"]]


def validate_date(date: str):
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    return date
