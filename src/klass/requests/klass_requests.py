from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any
from typing import TypedDict

import dateutil.parser
import pandas as pd
import requests
from typing_extensions import NotRequired

import klass.config as config
from klass.requests.sections import sections_dict
from klass.requests.validate import params_after
from klass.requests.validate import params_before
from klass.requests.validate import validate_params

# ##########
# Types #
# ##########

json_type = Any


class type_correspondenceTables(TypedDict):
    """The type returned by the version_by_id function."""

    name: str
    contactPerson: dict[str, str]
    owningSection: str
    lastModified: str
    published: list[str]
    source: NotRequired[str]
    sourceId: NotRequired[str]
    target: NotRequired[str]
    targetId: NotRequired[str]
    _links: dict[str, dict[str, str]]


def get_json(url: str, params: params_after) -> json_type:
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
    req = requests.Request("GET", url=url, headers=config.HEADERS, params=params)
    if config.TESTING:
        print("Full URL, check during testing:", req.prepare().url)
    response = requests.Session().send(req.prepare())
    response.raise_for_status()
    return response.json()


def convert_return_type(
    data: json_type, return_type: str = "pandas"
) -> Any | pd.DataFrame:
    """Differentiates between returning as raw json or convert to DataFrame."""
    if return_type == "json":
        return data
    return pd.json_normalize(data)


def convert_datestring(date: str | datetime, return_type: str = "isoklass") -> str:
    """Uses dateutil to guess the format of a time sent in, and convert it to the expected string format of the API."""
    if isinstance(date, str):
        date = dateutil.parser.parse(date)
    date_time = date.replace(tzinfo=timezone(timedelta(hours=1)))
    if return_type == "isoklass":
        return date_time.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + date.strftime("%z")
    elif return_type == "yyyy-mm-dd":
        return date_time.strftime("%Y-%m-%d")
    raise ValueError("Unrecognized datetimestring return type")


def convert_section(section: str) -> str:
    """Gets the full section-name-string (that the API needs) from just a provided section-number/numeric string."""
    if " " not in str(section):
        return sections_dict()[str(section)]
    return section


# ############
# ENDPOINTS #
# ############


def classifications(
    include_codelists: bool = False, changed_since: str = ""
) -> json_type:
    """Gets from the classifications-endpoint."""
    url = config.BASE_URL + "classifications"
    params: params_before = {
        "includeCodelists": include_codelists,
    }
    if changed_since == "":
        params["changedSince"] = convert_datestring(
            date=changed_since, return_type="isoklass"
        )
    params_final: params_after = validate_params(params)
    return get_json(url, params_final)


def classification_search(
    query: str = "", include_codelists: bool = False, ssbsection: str = ""
) -> json_type:
    """Gets from the classification/search-endpoint."""
    url = config.BASE_URL + "classifications/search"
    if not query:
        raise ValueError("Please specify a query")
    params: params_before = {
        "query": query,
        "includeCodelists": include_codelists,
    }
    if ssbsection:
        params["ssbSection"] = convert_section(ssbsection)
    params_final: params_after = validate_params(params)
    return get_json(url, params_final)


class type_version_part(TypedDict):
    """The type version part of the classification_by_id function."""

    version_id: NotRequired[int]
    name: str
    validFrom: str
    validTo: str
    lastModified: str
    published: list[str]
    _links: dict[str, dict[str, str]]


class type_json_classification_by_id(TypedDict):
    """The type returned by the classification_by_id function."""

    name: str
    classificationType: str
    lastModified: str
    description: str
    primaryLanguage: str
    copyrighted: bool
    includeShortName: bool
    includeNotes: bool
    contactPerson: dict[str, str]
    owningSection: str
    statisticalUnits: list[str]
    versions: list[type_version_part]
    _links: dict[str, dict[str, str]]


def classification_by_id(
    classification_id: str, language: str = "nb", include_future: bool = False
) -> type_json_classification_by_id:
    """Gets from the classification-by-id-endpoint."""
    url = config.BASE_URL + "classifications/" + str(classification_id)
    params: params_after = validate_params(
        {"language": language, "includeFuture": include_future}
    )
    result: type_json_classification_by_id = get_json(url, params)
    return result


def codes(
    classification_id: str,
    from_date: str,
    to_date: str = "",
    select_codes: str = "",
    select_level: str = "",
    presentation_name_pattern: str = "",
    language: str = "nb",
    include_future: bool = False,
) -> pd.DataFrame:
    """Gets from the codes-endpoint."""
    url = config.BASE_URL + "classifications/" + str(classification_id) + "/codes"
    from_date = convert_datestring(from_date, "yyyy-mm-dd")
    params: params_before = {
        "from": from_date,
    }
    if to_date:
        params["to"] = convert_datestring(to_date)
        params["to"] = to_date
    if select_codes:
        params["selectCodes"] = select_codes
    if select_level:
        params["selectLevel"] = select_level
    if presentation_name_pattern:
        params["presentationNamePattern"] = presentation_name_pattern
    if language:
        params["language"] = language
    if include_future:
        params["includeFuture"] = include_future
    params_final: params_after = validate_params(params)
    return convert_return_type(get_json(url, params_final)["codes"], "pandas")


def codes_at(
    classification_id: str,
    date: str,
    select_codes: str = "",
    select_level: str = "",
    presentation_name_pattern: str = "",
    language: str = "nb",
    include_future: bool = False,
) -> pd.DataFrame:
    """Gets from the codesAt-endpoint."""
    url = config.BASE_URL + "classifications/" + str(classification_id) + "/codesAt"
    date = convert_datestring(date, "yyyy-mm-dd")
    params: params_before = {"date": date}
    if select_codes:
        params["selectCodes"] = select_codes
    if select_level:
        params["selectLevel"] = select_level
    if presentation_name_pattern:
        params["presentationNamePattern"] = presentation_name_pattern
    if language:
        params["language"] = language
    if include_future:
        params["includeFuture"] = include_future
    params_final: params_after = validate_params(params)
    return convert_return_type(get_json(url, params_final)["codes"], "pandas")


class type_json_version_by_id(TypedDict):
    """The type returned by the version_by_id function."""

    name: str
    validFrom: str
    validTo: NotRequired[str]
    lastModified: str
    published: list[str]
    introduction: str
    contactPerson: dict[str, str]
    owningSection: str
    legalBase: NotRequired[str]
    publications: NotRequired[str]
    derivedFrom: NotRequired[str]
    correspondenceTables: list[type_correspondenceTables]
    classificationVariants: NotRequired[list[type_correspondenceTables]]
    changelogs: list[dict[str, str]]
    levels: list[dict[str, int | str]]
    classificationItems: list[dict[str, str | None]]
    _links: dict[str, dict[str, str]]


def version_by_id(
    version_id: str,
    language: str = "nb",
    include_future: bool = False,
) -> json_type:
    """Gets from the version-by-id-endpoint."""
    url = config.BASE_URL + "versions/" + str(version_id)
    params: params_after = validate_params(
        {
            "language": language,
            "includeFuture": include_future,
        }
    )
    result: type_json_version_by_id = get_json(url, params)
    return result


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
) -> pd.DataFrame | json_type:
    """Gets from the variant-endpoint."""
    url = config.BASE_URL + "classifications/" + str(classification_id) + "/variant"
    from_date = convert_datestring(from_date, "yyyy-mm-dd")
    params: params_before = {
        "variantName": variant_name,
        "from": from_date,
    }
    if to_date:
        params["to"] = convert_datestring(to_date, "yyyy-mm-dd")
    if select_codes:
        params["selectCodes"] = select_codes
    if select_level:
        params["selectLevel"] = select_level
    if presentation_name_pattern:
        params["presentationNamePattern"] = presentation_name_pattern
    if language:
        params["language"] = language
    if include_future:
        params["includeFuture"] = include_future
    params_final: params_after = validate_params(params)
    return convert_return_type(get_json(url, params_final)["codes"], return_type)


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
) -> pd.DataFrame | json_type:
    """Gets from the variantAt-endpoint."""
    url = config.BASE_URL + "classifications/" + str(classification_id) + "/variantAt"
    date = convert_datestring(date, "yyyy-mm-dd")
    params: params_before = {
        "variantName": variant_name,
        "date": date,
    }
    if select_codes:
        params["selectCodes"] = select_codes
    if select_level:
        params["selectLevel"] = select_level
    if presentation_name_pattern:
        params["presentationNamePattern"] = presentation_name_pattern
    if language:
        params["language"] = language
    if include_future:
        params["includeFuture"] = include_future

    params_final: params_after = validate_params(params)
    return convert_return_type(get_json(url, params_final)["codes"], return_type)


def variants_by_id(variant_id: str, language: str = "nb") -> json_type:
    """Gets from the variants-endpoint."""
    url = config.BASE_URL + "variants/" + str(variant_id)
    params: params_after = validate_params({"language": language})
    return get_json(url, params)


correspondanceItems_type = dict[str, str]


class type_json_corresponds(TypedDict):
    """The type returned by the corresponds function."""

    correspondenceItems: list[correspondanceItems_type]


def corresponds(
    source_classification_id: str,
    target_classification_id: str,
    from_date: str,
    to_date: str = "",
    language: str = "nb",
    include_future: bool = False,
) -> type_json_corresponds:
    """Gets from the classifications/corresponds-endpoint."""
    url = (
        config.BASE_URL
        + "classifications/"
        + str(source_classification_id)
        + "/corresponds"
    )
    from_date = convert_datestring(from_date, "yyyy-mm-dd")
    params: params_before = {
        "targetClassificationId": target_classification_id,
        "from": from_date,
    }
    if to_date:
        params["to"] = convert_datestring(to_date, "yyyy-mm-dd")
    if language:
        params["language"] = language
    if include_future:
        params["includeFuture"] = include_future
    params_final: params_after = validate_params(params)
    result: type_json_corresponds = get_json(url, params_final)
    return result


def corresponds_at(
    source_classification_id: str,
    target_classification_id: str,
    date: str,
    language: str = "nb",
    include_future: bool = False,
) -> type_json_corresponds:
    """Gets from the classificatins/correspondsAt-endpoint."""
    url = (
        config.BASE_URL
        + "classifications/"
        + str(source_classification_id)
        + "/correspondsAt"
    )
    date = convert_datestring(date, "yyyy-mm-dd")
    params: params_before = {
        "targetClassificationId": target_classification_id,
        "date": date,
    }
    if language:
        params["language"] = language
    if include_future:
        params["includeFuture"] = include_future
    params_final: params_after = validate_params(params)
    result: type_json_corresponds = get_json(url, params_final)
    return result


type_correspondanceMaps = list[dict[str, str]]


class type_json_correspondence_table_id(TypedDict):
    """The type returned by the correspondence_table_by_id function."""

    name: str
    contactPerson: dict[str, str]
    owningSection: str
    source: str
    sourceId: int
    target: str
    targetId: int
    changeTable: bool
    lastModified: str
    published: list[str]
    sourceLevel: str | None
    targetLevel: str | None
    description: str
    changelogs: list[str]
    correspondenceMaps: type_correspondanceMaps


def correspondence_table_by_id(
    correspondence_id: str,
    language: str = "nb",
) -> type_json_correspondence_table_id:
    """Gets from the correspondence-table-by-id-endpoint."""
    url = config.BASE_URL + "correspondencetables/" + str(correspondence_id)
    params: params_after = validate_params({"language": language})
    result_json: type_json_correspondence_table_id = get_json(url, params)
    return result_json


def changes(
    classification_id: str,
    from_date: str,
    to_date: str = "",
    language: str = "nb",
    include_future: bool = False,
    return_type: str = "pandas",
) -> pd.DataFrame | json_type:
    """Gets from the classifications/changes-endpoint."""
    url = (
        config.BASE_URL + "classifications/" + str(classification_id) + "/changes.json"
    )
    from_date = convert_datestring(from_date, "yyyy-mm-dd")
    if to_date:
        to_date = convert_datestring(to_date, "yyyy-mm-dd")
    params: params_before = {
        "from": from_date,
    }
    if to_date:
        params["to"] = to_date
    if language:
        params["language"] = language
    if include_future:
        params["includeFuture"] = include_future
    params_final: params_after = validate_params(params)
    return convert_return_type(get_json(url, params_final)["codeChanges"], return_type)


def classificationfamilies(
    ssbsection: str = "",
    include_codelists: bool = False,
    language: str = "nb",
) -> json_type:
    """Gets from the classificationfamilies-endpoint."""
    url = config.BASE_URL + "classificationfamilies"
    params: params_before = {
        "includeCodelists": include_codelists,
        "language": language,
    }
    if ssbsection:
        params["ssbSection"] = convert_section(ssbsection)
    params_final: params_after = validate_params(params)
    return get_json(url, params_final)


def classificationfamilies_by_id(
    classificationfamily_id: str,
    ssbsection: str = "",
    include_codelists: bool = False,
    language: str = "nb",
) -> json_type:
    """Gets from the classificationsfamilies-endpoint with id."""
    url = config.BASE_URL + "classificationfamilies/" + str(classificationfamily_id)
    params: params_before = {
        "includeCodelists": include_codelists,
        "language": language,
    }
    if ssbsection:
        params["ssbSection"] = convert_section(ssbsection)
    params_final: params_after = validate_params(params)
    return get_json(url, params_final)
