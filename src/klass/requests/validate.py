from datetime import datetime

import klass.config as config
from klass.requests.sections import sections_dict
from klass.requests.types import T_params_after
from klass.requests.types import T_params_before


def validate_params(params: T_params_before) -> T_params_after:
    """Links parameters to their validate-functions."""
    new_params: T_params_after = {}
    if "language" in params:
        new_params["language"] = validate_language(params["language"])
    if "includeFuture" in params:
        new_params["includeFuture"] = validate_bool(params["includeFuture"])
    if "from" in params:
        new_params["from"] = validate_date(params["from"])
    if "to" in params:
        new_params["to"] = validate_date(params["to"])
    if "date" in params:
        new_params["date"] = validate_date(params["date"])
    if "selectCodes" in params:
        new_params["selectCodes"] = validate_select_codes(params["selectCodes"])
    if "selectLevel" in params:
        new_params["selectLevel"] = validate_whole_number(params["selectLevel"])
    if "presentationNamePattern" in params:
        new_params["presentationNamePattern"] = validate_presentation_name_patterns(
            params["presentationNamePattern"]
        )
    if "variantName" in params:
        new_params["variantName"] = validate_alnum_spaces(params["variantName"])
    if "targetClassificationId" in params:
        new_params["targetClassificationId"] = validate_whole_number(
            params["targetClassificationId"]
        )
    if "ssbSection" in params:
        new_params["ssbSection"] = validate_ssb_section(params["ssbSection"])
    if "includeCodelists" in params:
        new_params["includeCodelists"] = validate_bool(params["includeCodelists"])
    if "changedSince" in params:
        new_params["changedSince"] = validate_time_iso8601(params["changedSince"])
    if "query" in params:
        new_params["query"] = validate_alnum_spaces(params["query"])

    return new_params


def validate_date(date: str) -> str:
    """Validate a date-string against the expected format."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError as e:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD") from e
    return date


def validate_language(language: str) -> str:
    """Validate the language-string against possible languages from the config."""
    language = language.lower()
    if language not in config.LANGUAGES:
        raise ValueError(
            f"Specify one of the valid languages: {', '.join(config.LANGUAGES)}"
        )
    return language


def validate_bool(val: bool) -> str:
    """Validate as a bool, then converts it to a lowercase string (required by API)."""
    if not isinstance(val, bool):
        raise TypeError(f"{val} needs to be a bool")
    val_return: str = str(val).lower()
    return val_return  # For some reason the parameters follow json-small-letter-bools


def validate_select_codes(codestring: str) -> str:
    """Select codes should only contain numbers, and some special characters."""
    codestring = codestring.replace(" ", "")
    check = codestring.replace("*", "").replace(",", "").replace("-", "")
    if not check.isdigit():
        raise ValueError(
            "Select-codes may only contain numbers and these special characters: *-,"
        )
    return codestring


def validate_whole_number(level: str) -> str:
    """Check that string is an int."""
    level = str(level)
    if not level.isdigit():
        raise ValueError("Select-levels must be a whole number")
    return level


def validate_presentation_name_patterns(pattern: str) -> str:
    """Name patters must be alphanumeric, except for some special chars."""
    remove = list(" {}/()-")
    check = "".join([c for c in pattern if c not in remove])
    if not check.isalpha():
        raise ValueError("Unexpected characters in presentation name pattern.")
    return pattern


def validate_alnum_spaces(variant_name: str) -> str:
    """Except for some other special characters, should be all alpha-numeric."""
    remove = list(" ()-")
    check = "".join([c for c in variant_name if c not in remove])
    if check not in ["", " "] and not check.isalnum():
        raise ValueError(
            "Expecting variant name to only include numbers, characters and spaces..."
        )
    return variant_name


def validate_time_iso8601(datestring: str) -> str:
    """Convert string to datetime, at the same time, datetime throws an error if format not matches."""
    datetime.strptime(datestring[:-5] + "000", "%Y-%m-%dT%H:%M:%S.%f")
    return datestring


def validate_ssb_section(section: str) -> str:
    """Check if the section sent in exists in the API."""
    section = str(section)
    sections = sections_dict()
    if section not in [*sections.keys(), *sections.values()]:
        raise ValueError(f"Cant find specified ssb-section {section}")
    return section
