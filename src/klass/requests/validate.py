import datetime

import dateutil

import klass.config as config
from klass.requests.sections import sections_dict
from klass.requests.types import ParamsAfterType
from klass.requests.types import ParamsBeforeType


def validate_params(params: ParamsBeforeType) -> ParamsAfterType:
    """Links parameters to their validate-functions."""
    new_params: ParamsAfterType = {}
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
        new_date: str = datetime.datetime.strptime(date, r"%Y-%m-%d").strftime(
            r"%Y-%m-%d"
        )
    except ValueError as e:
        try:
            new_date = dateutil.parser.parse(date).strftime(r"%Y-%m-%d")
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD") from e
    return new_date


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
    """Validate date-string by checking against datetime format YYYY-MM-DDThh:mm:ss.SSS+00:00.

    If no match, will try to convert it using dateutil.parser.parse to a datetime that includes milliseconds.
    """
    try_conversion = False
    try:
        datetime.datetime.strptime(datestring[:-5] + "000", "%Y-%m-%dT%H:%M:%S.%f%z")
    except Exception as e:
        try_conversion = True
        print(e)
    if (
        not datestring[-5:]
        .replace(".", "")
        .replace(":", "")
        .replace("+", "")
        .replace("-", "")
        .isnumeric()
    ):
        try_conversion = True
    if try_conversion:
        if datestring[-3] != ":":
            date_time = datetime.datetime.fromisoformat(
                datestring[:-2] + ":" + datestring[-2:]
            )
        else:
            date_time = datetime.datetime.fromisoformat(datestring)
        date_time.replace(tzinfo=datetime.timezone(datetime.timedelta(hours=1)))
        datestring = date_time.isoformat("T", "milliseconds")
    return datestring


def validate_ssb_section(section: str) -> str:
    """Check if the section sent in exists in the API."""
    section = str(section)
    sections = sections_dict()
    if section not in [*sections.keys(), *sections.values()]:
        raise ValueError(f"Cant find specified ssb-section {section}")
    return section
