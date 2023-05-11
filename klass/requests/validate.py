from datetime import datetime

from ..klass_config import LANGUAGES
from .sections import sections_dict


def validate_params(params: dict) -> dict:
    validations = {
        "language": validate_language,
        "includeFuture": validate_bool,
        "from": validate_date,
        "to": validate_date,
        "date": validate_date,
        "selectCodes": validate_select_codes,
        "selectLevel": validate_whole_number,
        "presentationNamePattern": validate_presentation_name_patterns,
        "variantName": validate_alnum_spaces,
        "targetClassificationId": validate_whole_number,
        "ssbSection": validate_ssb_section,
        "includeCodelists": validate_bool,
        "changedSince": validate_time_iso8601,
        "query": validate_alnum_spaces,
    }

    for param_key, param_value in params.items():
        params[param_key] = validations[param_key](param_value)

    return params


def validate_date(date: str) -> str:
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    return date


def validate_language(language: str) -> str:
    language = language.lower()
    if language not in LANGUAGES:
        raise ValueError(f"Specify one of the valid languages: {', '.join(LANGUAGES)}")
    return language


def validate_bool(val: bool) -> bool:
    if type(val) != bool:
        raise TypeError(f"{val} needs to be a bool")
    val = str(val).lower()
    return val  # For some reason the parameters follow json-small-letter-bools


def validate_select_codes(codestring: str) -> str:
    codestring = codestring.replace(" ", "")
    check = codestring.replace("*", "").replace(",", "").replace("-", "")
    if not check.isdigit():
        raise ValueError(
            "Select-codes may only contain numbers and these special characters: *-,"
        )
    return codestring


def validate_whole_number(level: str) -> str:
    level = str(level)
    if not level.isdigit():
        raise ValueError("Select-levels must be a whole number")
    return level


def validate_presentation_name_patterns(pattern: str) -> str:
    remove = list(" {}/()-")
    check = "".join([c for c in pattern if c not in remove])
    if not check.isalpha():
        raise ValueError("Unexpected characters in presentation name pattern.")
    return pattern


def validate_alnum_spaces(variant_name: str) -> str:
    check = variant_name.replace(" ", "")
    if not check.isalnum():
        raise ValueError(
            "Expecting variant name to only include numbers, characters and spaces..."
        )
    return variant_name


def validate_time_iso8601(datestring: str) -> str:
    datetime.strptime(datestring[:-5] + "000", "%Y-%m-%dT%H:%M:%S.%f")
    return datestring


def validate_ssb_section(section: str) -> str:
    section = str(section)
    sections = sections_dict()
    if section not in [*sections.keys(), *sections.values()]:
        raise ValueError(f"Cant find specified ssb-section {section}")
    return section
