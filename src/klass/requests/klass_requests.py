from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any

import dateutil.parser
import pandas as pd
import requests
from dateutil.parser import ParserError

import klass.config as config
from klass.requests.sections import sections_dict
from klass.requests.types import ClassificationFamiliesByIdType
from klass.requests.types import ClassificationFamiliesType
from klass.requests.types import ClassificationsByIdType
from klass.requests.types import ClassificationSearchType
from klass.requests.types import ClassificationsType
from klass.requests.types import CorrespondenceTableIdType
from klass.requests.types import CorrespondsType
from klass.requests.types import ParamsAfterType
from klass.requests.types import ParamsBeforeType
from klass.requests.types import VariantsByIdType
from klass.requests.types import VersionByIDType
from klass.requests.validate import validate_params

# ##########
# Types #
# ##########

URL_PART_CLASS = "classifications/"


def get_json(url: str, params: ParamsAfterType) -> Any:
    """Simplify getting the JSON out of a GET request to the KLASS API.

    Used in most of the following functions.

    Args:
        url (str): The URL to the endpoint.
        params (ParamsAfterType): The parameters to send to the endpoint.

    Returns:
        Any: The JSON response from the endpoint, hard to type because all endpoints have differently structured responses.
    """
    req = requests.Request("GET", url=url, headers=config.HEADERS, params=params)
    if config.TESTING:
        print("Full URL, check during testing:", req.prepare().url)
    response = requests.Session().send(req.prepare())
    response.raise_for_status()
    result: Any = response.json()
    return result


def convert_datestring(date: str | datetime, return_type: str = "isoklass") -> str:
    """First try dateutil to guess the format of a simple time sent in, secondary try the fromisoformat.

    Convert it to the expected string format of the API.
    """
    if isinstance(date, str):
        try:
            date_time: datetime = dateutil.parser.parse(date)
        except ParserError:
            date_time = datetime.fromisoformat(date)
    else:
        date_time = date
    date_time = date_time.replace(tzinfo=timezone(timedelta(hours=1)))
    if return_type == "isoklass":
        # We only want 3 digits of milliseconds.
        utc_offset = date_time.strftime("%z")
        if not utc_offset:
            utc_offset = "+00:00"
        elif utc_offset[-3] != ":":
            utc_offset = utc_offset[:-2] + ":" + utc_offset[-2:]
        return (
            date_time.strftime("%Y-%m-%dT%H:%M:%S.")
            + date_time.strftime("%f")[:3]
            + utc_offset
        )
    elif return_type == "yyyy-mm-dd":
        return date_time.strftime("%Y-%m-%d")
    raise ValueError(f"Unrecognized datetimestring return type: {date}")


def convert_section(section: str) -> str:
    """Get the full section-name-string (that the API needs) from just a provided section-number/numeric string."""
    if " " not in str(section):
        sections = sections_dict()
        return sections.get(
            str(section), "Section: {section} not in KLASS-sections? {sections}"
        )
    return section


# ###########
# ENDPOINTS #
# ###########


def classifications(
    include_codelists: bool = False, changed_since: str = ""
) -> ClassificationsType:
    """Get from the classifications-endpoint."""
    url = config.BASE_URL + "classifications"
    params: ParamsBeforeType = {
        "includeCodelists": include_codelists,
    }
    if changed_since != "":
        params["changedSince"] = convert_datestring(
            date=changed_since, return_type="isoklass"
        )
    params_final: ParamsAfterType = validate_params(params)
    result: ClassificationsType = get_json(url, params_final)
    return result


def classification_search(
    query: str = "", include_codelists: bool = False, ssbsection: str = ""
) -> ClassificationSearchType:
    """Get from the classification/search-endpoint."""
    url = config.BASE_URL + URL_PART_CLASS + "search"
    if not query:
        raise ValueError("Please specify a query")
    params: ParamsBeforeType = {
        "query": query,
        "includeCodelists": include_codelists,
    }
    if ssbsection:
        params["ssbSection"] = convert_section(ssbsection)
    params_final: ParamsAfterType = validate_params(params)
    result: ClassificationSearchType = get_json(url, params_final)
    return result


def classification_by_id(
    classification_id: str, language: str = "nb", include_future: bool = False
) -> ClassificationsByIdType:
    """Get from the classification-by-id-endpoint."""
    url = config.BASE_URL + URL_PART_CLASS + str(classification_id)
    params: ParamsAfterType = validate_params(
        {"language": language, "includeFuture": include_future}
    )
    result: ClassificationsByIdType = get_json(url, params)
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
    """Get from the codes-endpoint."""
    url = config.BASE_URL + URL_PART_CLASS + str(classification_id) + "/codes"
    from_date = convert_datestring(from_date, "yyyy-mm-dd")
    params: ParamsBeforeType = {
        "from": from_date,
    }
    if to_date:
        params["to"] = convert_datestring(to_date)
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
    params_final: ParamsAfterType = validate_params(params)
    return pd.json_normalize(get_json(url, params_final)["codes"])


def codes_at(
    classification_id: str,
    date: str,
    select_codes: str = "",
    select_level: str = "",
    presentation_name_pattern: str = "",
    language: str = "nb",
    include_future: bool = False,
) -> pd.DataFrame:
    """Get from the codesAt-endpoint."""
    url = config.BASE_URL + URL_PART_CLASS + str(classification_id) + "/codesAt"
    date = convert_datestring(date, "yyyy-mm-dd")
    params: ParamsBeforeType = {"date": date}
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
    params_final: ParamsAfterType = validate_params(params)
    return pd.json_normalize(get_json(url, params_final)["codes"])


def version_by_id(
    version_id: str,
    language: str = "nb",
    include_future: bool = False,
) -> VersionByIDType:
    """Get from the version-by-id-endpoint."""
    url = config.BASE_URL + "versions/" + str(version_id)
    params: ParamsAfterType = validate_params(
        {
            "language": language,
            "includeFuture": include_future,
        }
    )
    result: VersionByIDType = get_json(url, params)
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
) -> pd.DataFrame:
    """Get from the variant-endpoint."""
    url = config.BASE_URL + URL_PART_CLASS + str(classification_id) + "/variant"
    from_date = convert_datestring(from_date, "yyyy-mm-dd")
    params: ParamsBeforeType = {
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
    params_final: ParamsAfterType = validate_params(params)
    result: pd.DataFrame = pd.json_normalize(get_json(url, params_final)["codes"])
    return result


def variant_at(
    classification_id: str,
    variant_name: str,
    date: str,
    select_codes: str = "",
    select_level: str = "",
    presentation_name_pattern: str = "",
    language: str = "nb",
    include_future: bool = False,
) -> pd.DataFrame:
    """Get from the variantAt-endpoint."""
    url = config.BASE_URL + URL_PART_CLASS + str(classification_id) + "/variantAt"
    date = convert_datestring(date, "yyyy-mm-dd")
    params: ParamsBeforeType = {
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

    params_final: ParamsAfterType = validate_params(params)
    result: pd.DataFrame = pd.json_normalize(get_json(url, params_final)["codes"])
    return result


def variants_by_id(variant_id: str, language: str = "nb") -> VariantsByIdType:
    """Get from the variants-endpoint."""
    url = config.BASE_URL + "variants/" + str(variant_id)
    params: ParamsAfterType = validate_params({"language": language})
    result: VariantsByIdType = get_json(url, params)
    return result


def corresponds(
    source_classification_id: str,
    target_classification_id: str,
    from_date: str,
    to_date: str = "",
    language: str = "nb",
    include_future: bool = False,
) -> CorrespondsType:
    """Get from the classifications/corresponds-endpoint."""
    url = (
        config.BASE_URL
        + URL_PART_CLASS
        + str(source_classification_id)
        + "/corresponds"
    )
    from_date = convert_datestring(from_date, "yyyy-mm-dd")
    params: ParamsBeforeType = {
        "targetClassificationId": target_classification_id,
        "from": from_date,
    }
    if to_date:
        params["to"] = convert_datestring(to_date, "yyyy-mm-dd")
    if language:
        params["language"] = language
    if include_future:
        params["includeFuture"] = include_future
    params_final: ParamsAfterType = validate_params(params)
    result: CorrespondsType = get_json(url, params_final)
    return result


def corresponds_at(
    source_classification_id: str,
    target_classification_id: str,
    date: str,
    language: str = "nb",
    include_future: bool = False,
) -> CorrespondsType:
    """Get from the classificatins/correspondsAt-endpoint."""
    url = (
        config.BASE_URL
        + URL_PART_CLASS
        + str(source_classification_id)
        + "/correspondsAt"
    )
    date = convert_datestring(date, "yyyy-mm-dd")
    params: ParamsBeforeType = {
        "targetClassificationId": target_classification_id,
        "date": date,
    }
    if language:
        params["language"] = language
    if include_future:
        params["includeFuture"] = include_future
    params_final: ParamsAfterType = validate_params(params)
    result: CorrespondsType = get_json(url, params_final)
    return result


def correspondence_table_by_id(
    correspondence_id: str,
    language: str = "nb",
) -> CorrespondenceTableIdType:
    """Get from the correspondence-table-by-id-endpoint."""
    url = config.BASE_URL + "correspondencetables/" + str(correspondence_id)
    params: ParamsAfterType = validate_params({"language": language})
    result_json: CorrespondenceTableIdType = get_json(url, params)
    return result_json


def changes(
    classification_id: str,
    from_date: str,
    to_date: str = "",
    language: str = "nb",
    include_future: bool = False,
) -> pd.DataFrame:
    """Get from the classifications/changes-endpoint."""
    url = config.BASE_URL + URL_PART_CLASS + str(classification_id) + "/changes.json"
    from_date = convert_datestring(from_date, "yyyy-mm-dd")
    if to_date:
        to_date = convert_datestring(to_date, "yyyy-mm-dd")
    params: ParamsBeforeType = {
        "from": from_date,
    }
    if to_date:
        params["to"] = to_date
    if language:
        params["language"] = language
    if include_future:
        params["includeFuture"] = include_future
    params_final: ParamsAfterType = validate_params(params)
    result: pd.DataFrame = pd.json_normalize(get_json(url, params_final)["codeChanges"])
    return result


def classificationfamilies(
    ssbsection: str = "",
    include_codelists: bool = False,
    language: str = "nb",
) -> ClassificationFamiliesType:
    """Get from the classificationfamilies-endpoint."""
    url = config.BASE_URL + "classificationfamilies"
    params: ParamsBeforeType = {
        "includeCodelists": include_codelists,
        "language": language,
    }
    if ssbsection:
        params["ssbSection"] = convert_section(ssbsection)
    params_final: ParamsAfterType = validate_params(params)
    result: ClassificationFamiliesType = get_json(url, params_final)
    return result


def classificationfamilies_by_id(
    classificationfamily_id: str,
    ssbsection: str = "",
    include_codelists: bool = False,
    language: str = "nb",
) -> ClassificationFamiliesByIdType:
    """Get from the classificationsfamilies-endpoint with id."""
    url = config.BASE_URL + "classificationfamilies/" + str(classificationfamily_id)
    params: ParamsBeforeType = {
        "includeCodelists": include_codelists,
        "language": language,
    }
    if ssbsection:
        params["ssbSection"] = convert_section(ssbsection)
    params_final: ParamsAfterType = validate_params(params)
    result: ClassificationFamiliesByIdType = get_json(url, params_final)
    return result
