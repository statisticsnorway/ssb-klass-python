from datetime import datetime

import klass.klass_config as klass_config

from .sections import sections_dict


def validate_params(params: dict) -> dict:
    """Links parameters to their validate-functions."""
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
    """Validates a date-string against the expected format."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError as e:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD") from e
    return date


def validate_language(language: str) -> str:
    """Validates the language-string against possible languages from the config."""
    language = language.lower()
    if language not in klass_config.LANGUAGES:
        raise ValueError(
            f"Specify one of the valid languages: {', '.join(klass_config.LANGUAGES)}"
        )
    return language


def validate_bool(val: bool) -> bool:
    """Validates as a bool, then converts it to a lowercase string (required by API)."""
    if isinstance(val, bool):
        raise TypeError(f"{val} needs to be a bool")
    val = str(val).lower()
    return val  # For some reason the parameters follow json-small-letter-bools


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
    """Checks that string is an int."""
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
    """Converts string to datetime, at the same time, datetime throws an error if format not matches."""
    datetime.strptime(datestring[:-5] + "000", "%Y-%m-%dT%H:%M:%S.%f")
    return datestring


def validate_ssb_section(section: str) -> str:
    """Check if the section sent in exists in the API."""
    section = str(section)
    sections = sections_dict()
    if section not in [*sections.keys(), *sections.values()]:
        raise ValueError(f"Cant find specified ssb-section {section}")
    return section
