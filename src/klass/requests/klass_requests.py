from datetime import timedelta
from datetime import timezone

import dateutil.parser
import pandas as pd
import requests

from ..klass_config import KlassConfig
from .sections import sections_dict
from .validate import validate_params

# ##########
# GENERAL #
# ##########


def get_json(url: str, params: dict) -> dict:
    """Simplifies getting the json out of a get-request to the KLASS-api.

    Used in most of the following functions.

    Parameters
    ----------
    url : str
        The url to the endpoint.
    params : dict
        The parameters to send to the endpoint.

    Returns:
    -------
    dict
        The json-response from the endpoint.

    Raises:
    ------
    requests.exceptions.HTTPError
        If the response is not 200.
    requests.exceptions.RequestException
        If there is a connection-error.
    ValueError
        If the response has no json.
    """
    req = requests.Request("GET", url=url, headers=KlassConfig().HEADERS, params=params)
    if KlassConfig().TESTING:
        print("Full URL, check during testing:", req.prepare().url)
    response = requests.Session().send(req.prepare())
    response.raise_for_status()
    return response.json()


def convert_return_type(data: dict, return_type: str = "pandas") -> pd.DataFrame:
    """Differentiates between returning as raw json or convert to DataFrame."""
    if return_type == "json":
        return data
    return pd.json_normalize(data)


def convert_datestring(date: str, return_type: str = "isoklass") -> str:
    """Uses dateutil to guess the format of a time sent in, and convert it to the expected string format of the API."""
    if isinstance(date, str):
        date = dateutil.parser.parse(date)
    date = date.replace(tzinfo=timezone(timedelta(hours=1)))
    if return_type == "isoklass":
        return date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + date.strftime("%z")
    elif return_type == "yyyy-mm-dd":
        return date.strftime("%Y-%m-%d")
    raise ValueError("Unrecognized datetimestring return type")


def convert_section(section: str) -> str:
    """Gets the full section-name-string (that the API needs) from just a provided section-number/numeric string."""
    if " " not in str(section):
        return sections_dict()[str(section)]
    return section


# ############
# ENDPOINTS #
# ############


def classifications(include_codelists: bool = False, changed_since: str = "") -> dict:
    """Gets from the classifications-endpoint."""
    url = KlassConfig().BASE_URL + "classifications"
    params = {
        "includeCodelists": include_codelists,
    }
    if changed_since:
        params["changedSince"] = convert_datestring(changed_since, "isoklass")
    params = validate_params(params)
    return get_json(url, params)


def classification_search(
    query: str = "", include_codelists: bool = False, ssbsection: str = ""
) -> dict:
    """Gets from the classification/search-endpoint."""
    url = KlassConfig().BASE_URL + "classifications/search"
    if not query:
        raise ValueError("Please specify a query")
    params = {
        "query": query,
        "includeCodelists": include_codelists,
    }
    if ssbsection:
        params["ssbSection"] = convert_section(ssbsection)
    params = validate_params(params)
    return get_json(url, params)


def classification_by_id(
    classification_id: str,
    language: str = "nb",
    include_future: bool = False,
    return_type: str = "json",
) -> dict | pd.DataFrame:
    """Gets from the classification-by-id-endpoint."""
    url = KlassConfig().BASE_URL + "classifications/" + str(classification_id)
    params = validate_params({"language": language, "includeFuture": include_future})
    return convert_return_type(get_json(url, params), return_type)


def codes(
    classification_id: str,
    from_date: str,
    to_date: str = "",
    select_codes: str = "",
    select_level: str = "",
    presentation_name_pattern: str = "",
    language: str = "nb",
    include_future: bool = False,
    return_type: str = "pandas",
) -> pd.DataFrame | dict:
    """Gets from the codes-endpoint."""
    url = (
        KlassConfig().BASE_URL + "classifications/" + str(classification_id) + "/codes"
    )
    from_date = convert_datestring(from_date, "yyyy-mm-dd")
    params = {
        "from": from_date,
        "selectCodes": select_codes,
        "selectLevel": select_level,
        "presentationNamePattern": presentation_name_pattern,
        "language": language,
        "includeFuture": include_future,
    }
    if to_date:
        params["to"] = convert_datestring(to_date)
        params["to"] = to_date
    params = validate_params({k: v for k, v in params.items() if v != ""})
    return convert_return_type(get_json(url, params)["codes"], return_type)


def codes_at(
    classification_id: str,
    date: str,
    select_codes: str = "",
    select_level: str = "",
    presentation_name_pattern: str = "",
    language: str = "nb",
    include_future: bool = False,
    return_type: str = "pandas",
) -> pd.DataFrame | dict:
    """Gets from the codesAt-endpoint."""
    url = (
        KlassConfig().BASE_URL
        + "classifications/"
        + str(classification_id)
        + "/codesAt"
    )
    date = convert_datestring(date, "yyyy-mm-dd")
    params = {
        "date": date,
        "selectCodes": select_codes,
        "selectLevel": select_level,
        "presentationNamePattern": presentation_name_pattern,
        "language": language,
        "includeFuture": include_future,
    }
    params = validate_params({k: v for k, v in params.items() if v != ""})
    return convert_return_type(get_json(url, params)["codes"], return_type)


def version_by_id(
    version_id: str,
    language: str = "nb",
    include_future: bool = False,
    return_type: str = "json",
) -> dict | pd.DataFrame:
    """Gets from the version-by-id-endpoint."""
    url = KlassConfig().BASE_URL + "versions/" + str(version_id)
    params = validate_params(
        {
            "language": language,
            "includeFuture": include_future,
        }
    )
    return convert_return_type(get_json(url, params), return_type)


def variant(
    classification_id: str,
    variant_name: str,
    from_date: str,
    to_date: str = "",
    select_codes: str = "",
    select_level: str = "",
    presentation_name_pattern: str = "",
    language: str = "nb",
    include_future: bool = False,
    return_type: str = "pandas",
) -> pd.DataFrame | dict:
    """Gets from the variant-endpoint."""
    url = (
        KlassConfig().BASE_URL
        + "classifications/"
        + str(classification_id)
        + "/variant"
    )
    from_date = convert_datestring(from_date, "yyyy-mm-dd")
    params = {
        "variantName": variant_name,
        "from": from_date,
        "selectCodes": select_codes,
        "selectLevel": select_level,
        "presentationNamePattern": presentation_name_pattern,
        "language": language,
        "includeFuture": include_future,
    }
    if to_date:
        params["to"] = convert_datestring(to_date, "yyyy-mm-dd")
    params = validate_params({k: v for k, v in params.items() if v != ""})
    print(params)
    return convert_return_type(get_json(url, params)["codes"], return_type)


def variant_at(
    classification_id: str,
    variant_name: str,
    date: str,
    select_codes: str = "",
    select_level: str = "",
    presentation_name_pattern: str = "",
    language: str = "nb",
    include_future: bool = False,
    return_type: str = "pandas",
) -> pd.DataFrame | dict:
    """Gets from the variantAt-endpoint."""
    url = (
        KlassConfig().BASE_URL
        + "classifications/"
        + str(classification_id)
        + "/variantAt"
    )
    date = convert_datestring(date, "yyyy-mm-dd")
    params = {
        "variantName": variant_name,
        "date": date,
        "selectCodes": select_codes,
        "selectLevel": select_level,
        "presentationNamePattern": presentation_name_pattern,
        "language": language,
        "includeFuture": include_future,
    }
    params = validate_params({k: v for k, v in params.items() if v not in ["", ("",)]})
    return convert_return_type(get_json(url, params)["codes"], return_type)


def variants_by_id(
    variant_id: str, language: str = "nb", return_type: str = "json"
) -> dict | pd.DataFrame:
    """Gets from the variants-endpoint."""
    url = KlassConfig().BASE_URL + "variants/" + str(variant_id)
    params = validate_params({"language": language})
    return convert_return_type(get_json(url, params), return_type)


def corresponds(
    source_classification_id: str,
    target_classification_id: str,
    from_date: str,
    to_date: str = "",
    language: str = "nb",
    include_future: bool = False,
    return_type: str = "json",
) -> dict | pd.DataFrame:
    """Gets from the classifications/corresponds-endpoint."""
    url = (
        KlassConfig().BASE_URL
        + "classifications/"
        + str(source_classification_id)
        + "/corresponds"
    )
    from_date = convert_datestring(from_date, "yyyy-mm-dd")
    params = {
        "targetClassificationId": target_classification_id,
        "from": from_date,
        "language": language,
        "includeFuture": include_future,
    }
    if to_date:
        params["to"] = convert_datestring(to_date, "yyyy-mm-dd")
    params = validate_params({k: v for k, v in params.items() if v != ""})

    return convert_return_type(get_json(url, params), return_type)


def corresponds_at(
    source_classification_id: str,
    target_classification_id: str,
    date: str,
    language: str = "nb",
    include_future: bool = False,
    return_type: str = "json",
) -> dict | pd.DataFrame:
    """Gets from the classificatins/correspondsAt-endpoint."""
    url = (
        KlassConfig().BASE_URL
        + "classifications/"
        + str(source_classification_id)
        + "/correspondsAt"
    )
    date = convert_datestring(date, "yyyy-mm-dd")
    params = {
        "targetClassificationId": target_classification_id,
        "date": date,
        "language": language,
        "includeFuture": include_future,
    }
    params = validate_params({k: v for k, v in params.items() if v != ""})
    return convert_return_type(get_json(url, params), return_type)


def correspondence_table_by_id(
    correspondence_id: str, language: str = "nb", return_type: str = "json"
) -> dict | pd.DataFrame:
    """Gets from the correspondence-table-by-id-endpoint."""
    url = KlassConfig().BASE_URL + "correspondencetables/" + str(correspondence_id)
    params = validate_params({"language": language})
    return convert_return_type(get_json(url, params), return_type)


def changes(
    classification_id: str,
    from_date: str,
    to_date: str = "",
    language: str = "nb",
    include_future: bool = False,
    return_type: str = "pandas",
) -> pd.DataFrame | dict:
    """Gets from the classifications/changes-endpoint."""
    url = (
        KlassConfig().BASE_URL
        + "classifications/"
        + str(classification_id)
        + "/changes.json"
    )
    from_date = convert_datestring(from_date, "yyyy-mm-dd")
    if to_date:
        to_date = convert_datestring(to_date, "yyyy-mm-dd")
    params = {
        "from": from_date,
        "to": to_date,
        "language": language,
        "includeFuture": include_future,
    }
    params = validate_params({k: v for k, v in params.items() if v != ""})
    return convert_return_type(get_json(url, params)["codeChanges"], return_type)


def classificationfamilies(
    ssbsection: str = "",
    include_codelists: bool = False,
    language: str = "nb",
) -> dict:
    """Gets from the classificationfamilies-endpoint."""
    url = KlassConfig().BASE_URL + "classificationfamilies"
    params = {"includeCodelists": include_codelists, "language": language}
    if ssbsection:
        params["ssbSection"] = convert_section(ssbsection)
    params = validate_params(params)
    return get_json(url, params)


def classificationfamilies_by_id(
    classificationfamily_id: str,
    ssbsection: str = "",
    include_codelists: bool = False,
    language: str = "nb",
) -> dict:
    """Gets from the classificationsfamilies-endpoint with id."""
    url = (
        KlassConfig().BASE_URL
        + "classificationfamilies/"
        + str(classificationfamily_id)
    )
    params = {"includeCodelists": include_codelists, "language": language}
    if ssbsection:
        params["ssbSection"] = convert_section(ssbsection)
    params = validate_params(params)
    return get_json(url, params)
