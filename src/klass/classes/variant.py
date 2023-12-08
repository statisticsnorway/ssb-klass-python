import pandas as pd

from klass.requests.klass_requests import variant
from klass.requests.klass_requests import variant_at
from klass.requests.klass_requests import variants_by_id
from klass.requests.types import CorrespondenceTablesType
from klass.requests.types import VariantsByIdType


class KlassVariant:
    """In Klass a Variant is a different way of aggregating an existing codelist.

    It does not have to be extensive (all filled out), but can, for example,
    redefine upper levels, for some lower-level codes.

    For example:
    "Study points for vocational education programmes" is a Version (ID 1959)
    for the Classification of Education (NUS, ID 36).
    It sets a new upper level of codes (amount of study points),
    for a set of lower-level existing codes (NUS codes, level 5).

    Attributes:
        data (pd.DataFrame): The classificationItems as a pandas dataframe. Usually what you're after?
        variant_id (str): The variant_id of the variant. For example: '36'.
        name (str): The name of the variant.
        contactPerson (dict): The contact person of the variant.
        owningSection (str): The owning section of the variant.
        lastModified (str): Stringified iso-datetime for last modification.
        published (list[str]): Languages that the variant is published in.
        validFrom (str): Date-string from when the version is valid.
        validTo (str, optional): Date-string to when the version is valid.
        introduction (str): A longer description of the variant.
        correspondenceTables (list): The correspondence tables of the variant.
        changelogs (list): The changelogs of the variant.
        levels (list[dict]): The levels contained in the codelist (items).
        classificationItems (list[dict]): The codelist-elements of the variant.
        select_level (int): The level of the dataset to keep. For example: 0.
        language (str): The language of the variant to select. For example: 'nb'.
        _links (dict): The links returned from the API.

    Args:
        variant_id (str): The variant_id of the variant. For example: '1959'.
        select_level (int): The level of the dataset to keep. For example: 5.
        language (str): The language of the variant to select. For example: 'nb'.
    """

    def __init__(
        self,
        variant_id: str,
        select_level: int = 0,
        language: str = "nb",
    ):
        """Get the data from the KLASS-api to populate this objects attributes."""
        self.variant_id = variant_id
        self.select_level = select_level
        self.language = language

        self.get_classification_codes()

    def get_classification_codes(self, select_level: int = 0) -> None:
        """Get the data from the API, setting it as attributes on the object.

        The codes are put into the .data attribute.
        Other keys are added dynamically to the object, like classificationItems.

        Args:
            select_level (int): The level of the dataset to keep. For example: 0.
        """
        result: VariantsByIdType = variants_by_id(self.variant_id, self.language)
        self.name: str = result["name"]
        if "validTo" in result:
            self.validTo: str = result["validTo"]
        if "legalBase" in result:
            self.legalBase: str = result["legalBase"]
        if "publications" in result:
            self.publications: str = result["publications"]
        if "derivedFrom" in result:
            self.derivedFrom: str = result["derivedFrom"]
        self.contactPerson: dict[str, str] = result["contactPerson"]
        self.owningSection: str = result["owningSection"]
        self.lastModified: str = result["lastModified"]
        self.published: list[str] = result["published"]
        self.validFrom: str = result["validFrom"]
        self.introduction: str = result["introduction"]
        self.correspondenceTables: list[CorrespondenceTablesType] = result[
            "correspondenceTables"
        ]
        self.changelogs: list[dict[str, str]] = result["changelogs"]
        self.levels: list[dict[str, int | str]] = result["levels"]
        self.classificationItems: list[dict[str, str | None]] = result[
            "classificationItems"
        ]
        self._links: dict[str, dict[str, str]] = result["_links"]

        df = pd.json_normalize(self.classificationItems)
        if not select_level and self.select_level:
            select_level = self.select_level
        if select_level:
            self.data = df[df["level"] == str(select_level)]
        else:
            self.data = df

    def __repr__(self) -> str:
        """Get a string representation of how to recreate the current object, including set parameters."""
        result = f"KlassVariant(variant_id={self.variant_id}, "
        if self.select_level:
            result += f"select_level={self.select_level}, "
        if self.language != "nb":
            result += f"language={self.language}"
        result += ")"
        return result

    def __str__(self) -> str:
        """Print a human readable string of the object, including its ID and a preview of the data contained."""
        result = f"This is a Klass Variant with the ID of {self.variant_id}."
        result += f"\nPreview of the .data (5 first rows):\n{self.data[self.data.columns[:5]].head(5)}"
        return result


class KlassVariantSearchByName:
    """Look up a Variant based on the owning Classifications ID and the start of the Variants name.

    The name is put into a URL-parameter, so it might be sensitive to special characters,
    if the name you are trying isn't working, try keeping less of it, but keep the start of the name.

    There might be a bug (2023), where you can get duplicate rows from the API on this,
    so if you use this class, make sure to check for duplicates before moving on.

    In Klass a Variant is a different way of aggregating an existing codelist.
    It does not have to be extensive (all filled out), but can, for example,
    redefine upper levels, for some lower-level codes.

    Attributes:
        data (pd.DataFrame): The codelists from the Variant as a pandas dataframe. Usually what you're after?
        classification_id (str): The classification ID.
        variant_name (str): The start of the variant name.
        from_date (str): The start of the date range.
        to_date (str): The end of the date range.
        select_codes (str): Limit the result to codes matching this pattern.
            See rules: https://data.ssb.no/api/klass/v1/api-guide.html#_selectcodes
        select_level (str): The level of codes to keep in the dataset.
        presentation_name_pattern (str): Used to build an alternative presentation name for the codes.
            See rules: https://data.ssb.no/api/klass/v1/api-guide.html#_presentationnamepattern
        language (str): Language of the names, select "en", "nb" or "nn".
        include_future (bool): Whether to include future codes. Defaults to False.

    Args:
        classification_id (str): The classification ID.
        variant_name (str): The start of the variant name.
        from_date (str): The start of the date range.
        to_date (str): The end of the date range.
        select_codes (str): Limit the result to codes matching this pattern.
            See rules: https://data.ssb.no/api/klass/v1/api-guide.html#_selectcodes
        select_level (str): The level of codes to keep in the dataset.
        presentation_name_pattern (str): Used to build an alternative presentation name for the codes.
            See rules: https://data.ssb.no/api/klass/v1/api-guide.html#_presentationnamepattern
        language (str): Language of the names, select "en", "nb" or "nn".
        include_future (bool): Whether to include future codes. Defaults to False.
    """

    def __init__(
        self,
        classification_id: str,
        variant_name: str,
        from_date: str,
        to_date: str = "",
        select_codes: str = "",
        select_level: str = "",
        presentation_name_pattern: str = "",
        language: str = "nb",
        include_future: bool = False,
    ):
        """Get the data from the KLASS-api, setting it as attributes on the object."""
        self.classification_id = classification_id
        self.variant_name = variant_name
        self.from_date = from_date
        self.to_date = to_date
        self.select_codes = select_codes
        self.select_level = select_level
        self.presentation_name_pattern = presentation_name_pattern
        self.language = language
        self.include_future = include_future
        self.get_variant()

    def get_variant(self) -> None:
        """Actually get the data from the API, called at the end of init."""
        if self.to_date:
            self.data = variant(
                classification_id=self.classification_id,
                variant_name=self.variant_name,
                from_date=self.from_date,
                to_date=self.to_date,
                select_codes=self.select_codes,
                select_level=self.select_level,
                presentation_name_pattern=self.presentation_name_pattern,
                language=self.language,
                include_future=self.include_future,
            )
        else:
            self.data = variant_at(
                classification_id=self.classification_id,
                variant_name=self.variant_name,
                date=self.from_date,
                select_codes=self.select_codes,
                select_level=self.select_level,
                presentation_name_pattern=self.presentation_name_pattern,
                language=self.language,
                include_future=self.include_future,
            )

    def __repr__(self) -> str:
        """Get a string representation of how to recreate the current object, including set parameters."""
        result = (
            f'KlassVariantSearchByName(classification_id="{self.classification_id}", '
        )
        result += f'variant_name="{self.variant_name}", from_date="{self.from_date}", '
        if self.to_date:
            result += f'to_date="{self.to_date}", '
        if self.select_codes:
            result += f'select_codes="{self.select_codes}", '
        if self.select_level:
            result += f'select_level="{self.select_level}", '
        if self.presentation_name_pattern:
            result += f'presentation_name_pattern="{self.presentation_name_pattern}", '
        if self.language != "nb":
            result += f'language="{self.language}", '
        if self.include_future:
            result += f"include_future={self.include_future}"
        result += ")"
        return result

    def __str__(self) -> str:
        """Print a human-readable representation of the the object, including a preview of its data."""
        result = f'A search for variants on classification ID "{self.classification_id}" on the name "{self.variant_name}".\n'
        result += f"From the date {self.from_date}"
        if self.to_date:
            result += f", to the date {self.to_date}"
        result += f".\nPreview of the .data (frist 5 rows):\n{self.data[self.data.columns[:5]].head(5)}"
        return result
