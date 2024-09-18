from typing import TypedDict

from typing_extensions import NotRequired

# Keeping these two as non-class, declarative, as the API operates with the parameter "from", which is a reserved keyword in Python
ParamsBeforeType = TypedDict(
    "ParamsBeforeType",
    {
        "language": NotRequired[str],
        "includeFuture": NotRequired[bool],  # Will be converted to lowercase string
        "from": NotRequired[str],  # Cant convert to class cause of this thingy
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
ParamsAfterType = TypedDict(
    "ParamsAfterType",
    {
        "language": NotRequired[str],
        "includeFuture": NotRequired[str],
        "from": NotRequired[str],  # Cant convert to class cause of this thingy
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


class CorrespondenceTablesType(TypedDict):
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


class VersionPartType(TypedDict):
    """The type version part of the classification_by_id function."""

    version_id: NotRequired[int]
    name: str
    validFrom: str
    validTo: str
    lastModified: str
    published: list[str]
    _links: dict[str, dict[str, str]]


class VariantsByIdType(TypedDict):
    """The type returned by the variants_by_id function."""

    validTo: NotRequired[str]
    legalBase: NotRequired[str]
    publications: NotRequired[str]
    derivedFrom: NotRequired[str]
    name: str
    contactPerson: dict[str, str]
    owningSection: str
    lastModified: str
    published: list[str]
    validFrom: str
    introduction: str
    correspondenceTables: list[CorrespondenceTablesType]
    changelogs: list[dict[str, str]]
    levels: list[dict[str, int | str]]
    classificationItems: list[dict[str, str | None]]
    _links: dict[str, dict[str, str]]


class ClassificationPartWithType(TypedDict):
    """Type for each of the classifications returned by a classificationfamilies-search."""

    classification_id: NotRequired[str]
    name: str
    classificationType: str
    lastModified: str
    _links: dict[str, dict[str, str]]


class ClassificationsType(TypedDict):
    """The type returned by the classifications function."""

    _embedded: dict[str, list[ClassificationPartWithType]]
    _links: dict[str, dict[str, str]]
    page: dict[str, int]


class ClassificationsByIdType(TypedDict):
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
    versions: list[VersionPartType]
    _links: dict[str, dict[str, str]]


class ClassificationSearchResultsPartType(TypedDict):
    """Type for each of the classifications returned by a classificationfamilies-search."""

    classification_id: NotRequired[int]
    name: str
    snippet: str
    searchScore: float
    _links: dict[str, dict[str, str]]


class ClassificationSearchType(TypedDict):
    """The type returned by the classification_search function."""

    _embedded: NotRequired[dict[str, list[ClassificationSearchResultsPartType]]]
    _links: dict[str, dict[str, str]]
    page: dict[str, int]


class VersionByIDType(TypedDict):
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
    correspondenceTables: list[CorrespondenceTablesType]
    classificationVariants: NotRequired[list[CorrespondenceTablesType]]
    changelogs: list[dict[str, str]]
    levels: list[dict[str, int | str]]
    classificationItems: list[dict[str, str | None]]
    _links: dict[str, dict[str, str]]


T_correspondanceItems = dict[str, str]


class CorrespondsType(TypedDict):
    """The type returned by the corresponds function."""

    correspondenceItems: list[T_correspondanceItems]


T_correspondanceMaps = list[dict[str, str]]


class CorrespondenceTableIdType(TypedDict):
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


class ClassificationFamiliesPartWithNumberType(TypedDict):
    """Type for each of the classifications returned by a classificationfamilies-search."""

    family_id: NotRequired[str]
    name: str
    numberOfClassifications: int
    _links: dict[str, dict[str, str]]


class ClassificationFamiliesType(TypedDict):
    """The type returned by the classificationfamilies function."""

    _embedded: NotRequired[dict[str, list[ClassificationFamiliesPartWithNumberType]]]
    _links: dict[str, dict[str, str]]


class ClassificationFamiliesByIdType(TypedDict):
    """Type for the whole return value of a classificationfamilies-search."""

    name: str
    classifications: list[ClassificationPartWithType]
    _links: dict[str, dict[str, str]]
