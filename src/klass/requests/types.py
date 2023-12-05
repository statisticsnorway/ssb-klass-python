from typing import NotRequired
from typing import TypedDict

T_params_before = TypedDict(
    "params_before",
    {
        "language": NotRequired[str],
        "includeFuture": NotRequired[bool],  # Will be converted to lowercase string
        "from": NotRequired[str],
        "to": NotRequired[str],
        "date": NotRequired[str],
        "selectCodes": NotRequired[str],
        "selectLevel": NotRequired[str],
        "presentationNamePattern": NotRequired[str],
        "variantName": NotRequired[str],
        "targetClassificationId": NotRequired[str],
        "ssbSection": NotRequired[str],
        "includeCodelists": NotRequired[bool],  # Will be converted to lowercase string
        "changedSince": NotRequired[str],
        "query": NotRequired[str],
    },
)
T_params_after = TypedDict(
    "params_after",
    {
        "language": NotRequired[str],
        "includeFuture": NotRequired[str],
        "from": NotRequired[str],
        "to": NotRequired[str],
        "date": NotRequired[str],
        "selectCodes": NotRequired[str],
        "selectLevel": NotRequired[str],
        "presentationNamePattern": NotRequired[str],
        "variantName": NotRequired[str],
        "targetClassificationId": NotRequired[str],
        "ssbSection": NotRequired[str],
        "includeCodelists": NotRequired[str],
        "changedSince": NotRequired[str],
        "query": NotRequired[str],
    },
)


class T_correspondenceTables(TypedDict):
    """The type in the correspondanceTables attribute."""

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


class T_version_part(TypedDict):
    """The type version part of the classification_by_id function."""

    version_id: NotRequired[int]
    name: str
    validFrom: str
    validTo: str
    lastModified: str
    published: list[str]
    _links: dict[str, dict[str, str]]


class T_classification_by_id(TypedDict):
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
    versions: list[T_version_part]
    _links: dict[str, dict[str, str]]


class T_version_by_id(TypedDict):
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
    correspondenceTables: list[T_correspondenceTables]
    classificationVariants: NotRequired[list[T_correspondenceTables]]
    changelogs: list[dict[str, str]]
    levels: list[dict[str, int | str]]
    classificationItems: list[dict[str, str | None]]
    _links: dict[str, dict[str, str]]


T_correspondanceItems = dict[str, str]


class T_corresponds(TypedDict):
    """The type returned by the corresponds function."""

    correspondenceItems: list[T_correspondanceItems]


T_correspondanceMaps = list[dict[str, str]]


class T_correspondence_table_id(TypedDict):
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
    correspondenceMaps: T_correspondanceMaps


class T_classificationfamilies_by_id_classifications(TypedDict):
    """Type for each of the classifications returned by a classificationfamilies-search."""

    classification_id: NotRequired[str]
    name: str
    classificationType: str
    lastModified: str
    _links: dict[str, dict[str, str]]


class T_classificationfamilies_by_id(TypedDict):
    """Type for the whole return value of a classificationfamilies-search."""

    name: str
    classifications: list[T_classificationfamilies_by_id_classifications]
    _links: dict[str, dict[str, str]]
