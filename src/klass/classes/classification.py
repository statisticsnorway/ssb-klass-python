from typing import Literal

import pandas as pd
from typing_extensions import Self

from ..requests.klass_requests import changes
from ..requests.klass_requests import classification_by_id
from ..requests.klass_types import ClassificationsByIdType
from ..requests.klass_types import Language
from ..requests.klass_types import OptionalLanguage
from ..requests.klass_types import VersionPartType
from .codes import KlassCodes
from .correspondence import KlassCorrespondence
from .variant import KlassVariant
from .variant import KlassVariantSearchByName
from .version import KlassVersion


class KlassClassification:
    """Classifications are the main level people are used to thinking about "things in KLASS".

    - they represent "groupings of general, official codelists".
    - can have many Versions, versions are the classification placed in time. When the classification is updated with new codes, a new version is created.
    - has Codes, actually owned by the Versions (placed in time), but they are directly available under the classification as well, by adding time-parameters.
    - has Variants, which are differently grouped aggregations of codelists.
    - can Correspond with other Classifications and their codelists.
    - belongs undera Family, a general statistical group, like "Education".


    Print an initialized Classification object to see extensive information.

    To see all the Classification's Variants (different aggregations of codelists),
    you first need to get the classification at a specific time (a KlassVersion)
    by using get_version() for example.

    Attributes:
        versions (list): A list of the data the Classifications has on its versions.
            Versions represent the changes to the classifications codelists placed in time.
        name (str): The name of the classification.
        classification_id (str): The ID of the classification.
        classificationType (str): The type of the classification.
        lastModified (str): The last time the classification was modified. ISO-stringified datetime(ISO-datetime)
        description (str): A longer description of the classification.
        primaryLanguage (str): The primary language of the classification. "nb", "nn" or "en".
        language (str): The language chosen at initialization of the classification. "nb", "nn" or "en".
        copyrighted (bool): Whether the classification is copyrighted.
        includeShortName (bool): If true, indicates that classificationItems may have shortnames.
        includeNotes (bool): If true, indicates that classificationItems may have notes.
        contactPerson (dict): A dictionary containing the contact person of the classification.
        owningSection (str): The section (part of Statistics Norway)that owns the classification.
        statisticalUnits (list): Statistical units assigned to classification
        include_future (bool): Whether to include future versions of the classification.
        _links (dict): A dictionary containing the links to different possible endpoints using the classification.

    Args:
        classification_id: The classification_id of the classification. For example: '36'
        language: The language of the classification. "nb", "nn" or "en".
        include_future: Whether to include future versions of the classification.

    Raises:
        ValueError: If the language is not "no", "nb" or "en".
            If the include_future is not a bool.
    """

    def __init__(
        self: Self,
        classification_id: str | int,
        language: Language = "nb",
        include_future: bool = False,
    ) -> None:
        """Get the data for the classification from the API."""
        self.classification_id = classification_id
        self.language: Language = language
        self.include_future = include_future
        result: ClassificationsByIdType = classification_by_id(
            classification_id, language=language, include_future=include_future
        )
        self.name: str = result.get("name", "")
        self.classificationType: str = result.get("classificationType", "")
        self.lastModified: str = result.get("lastModified", "")
        self.description: str = result.get("description", "")
        self.primaryLanguage: Language | Literal[""] = result.get("primaryLanguage", "")
        self.copyrighted: bool = result.get("copyrighted", True)
        self.includeShortName: bool = result.get("includeShortName", False)
        self.includeNotes: bool = result.get("includeNotes", False)
        self.contactPerson: dict[str, str] = result.get("contactPerson", {})
        self.owningSection: str = result.get("owningSection", "")
        self.statisticalUnits: list[str] = result.get("statisticalUnits", [""])
        versions_temp: list[VersionPartType] = result.get("versions", [])
        self._links: dict[str, dict[str, str]] = result.get("_links", {})

        version_replace: list[VersionPartType] = []
        for ver in versions_temp:
            version_replace.append(
                {"version_id": int(ver["_links"]["self"]["href"].split("/")[-1]), **ver}
            )

        self.versions: list[VersionPartType] = version_replace

    def __str__(self) -> str:
        """Print a readable string of the classification, including some of its attributes."""
        contact = "Contact Person:\n"
        for k, v in self.contactPerson.items():
            contact += f"\t{k}: {v}\n"
        units = ", ".join(self.statisticalUnits)
        result = f"""Classification {self.classification_id}: {self.name}
        Owning Section: {self.owningSection}
        {contact}
        Statistical Units: {units}
        Number of versions: {len(self.versions)}

{self.description}
        """
        return result

    def __repr__(self) -> str:
        """Return a copy-pasteable string to recreate the object."""
        result = f"KlassClassification(classification_id='{self.classification_id}', "
        if self.language != "nb":
            result += f"language='{self.language}', "
        if self.include_future:
            result += "include_future=True, "
        result += ")"
        return result

    def get_version(
        self,
        version_id: int | None = None,
        select_level: int | None = None,
        language: OptionalLanguage = None,
        include_future: bool | None = None,
    ) -> KlassVersion:
        """Return a KlassVersion object of the classification based on ID.

        A Version in Klass is a Classification placed in time.
        If no ID is specified, will get the first version under the attribute .versions on this class.

        Args:
            version_id: The version ID of the version.
            select_level: The level of the version to keep in the data.
            language: The language of the version. "nn", "nb" or "en".
            include_future: Whether to include future versions of the version.

        Returns:
            KlassVersion: A KlassVersion object of the specified ID.
        """
        if not version_id:
            version_id = sorted(self.versions, key=lambda x: x["validFrom"])[-1][
                "version_id"
            ]
        if not language:
            language = self.language
        if include_future is None:
            include_future = self.include_future
        return KlassVersion(
            str(version_id),
            select_level=select_level,
            language=language,
            include_future=include_future,
        )

    def versions_dict(self) -> dict[int, str]:
        """Reformats the versions into a simple dict with just the IDs as keys and names as values.

        Returns:
            dict: Version IDs as keys, and version names as values.
        """
        return {v["version_id"]: v["name"] for v in self.versions[::-1]}

    def get_variant_by_name(
        self,
        name: str,
        from_date: str,
        to_date: str | None = None,
        select_codes: str | None = None,
        select_level: int | None = None,
        presentation_name_pattern: str | None = None,
        language: Language = "nb",
        include_future: bool = False,
    ) -> KlassVariantSearchByName:
        """Get a KlassVariant by searching for its name under the Variants owned by the current classification.

        In Klass, a Variant is a different way of aggregating an existing codelist.
        It does not have to be extensive (all filled out), but can, for example,
        redefine upper levels for some lower-level codes.

        Args:
            name: The start of the name of the variant.
            from_date: The start date of the time period. "YYYY-MM-DD".
            to_date: The end date of the time period. "YYYY-MM-DD".
            select_codes: Limit the result to codes matching this pattern.
                See rules: https://data.ssb.no/api/klass/v1/api-guide.html#_selectcodes.
            select_level: The level of the version to keep in the data.
            presentation_name_pattern: Used to build an alternative presentation name for the codes.
                See rules: https://data.ssb.no/api/klass/v1/api-guide.html#_presentationnamepattern.
            language: The language of the version. "nn", "nb" or "en".
            include_future: Whether to include future versions of the version.

        Returns:
            KlassVariantSearchByName: A KlassVariantSearchByName object based on the classification's ID
            and searching for the name passed in.
        """
        return KlassVariantSearchByName(
            classification_id=self.classification_id,
            variant_name=name,
            from_date=from_date,
            to_date=to_date,
            select_codes=select_codes,
            select_level=select_level,
            presentation_name_pattern=presentation_name_pattern,
            language=language,
            include_future=include_future,
        )

    def get_correspondence_to(
        self,
        target_classification_id: str | int,
        from_date: str,
        to_date: str | None = None,
        language: OptionalLanguage = None,
        include_future: bool | None = None,
    ) -> KlassCorrespondence:
        """Treats the current classification as a source of correspondences, specifying the target's ID and a date.

        Returns a KlassCorrespondence object of the correspondences.

        Args:
            target_classification_id: The classification ID of the target classification.
            from_date: The start date of the time period. "YYYY-MM-DD".
            to_date: The end date of the time period. "YYYY-MM-DD".
            language: The language of the correspondences. "nn", "nb" or "en".
            include_future: Whether to include future correspondences.

        Returns:
            KlassCorrespondence: A KlassCorrespondence object of the correspondences
            between the current classification and the target classification.
        """
        if not language:
            language = self.language
        if include_future is None:
            include_future = self.include_future
        return KlassCorrespondence(
            source_classification_id=self.classification_id,
            target_classification_id=target_classification_id,
            from_date=from_date,
            to_date=to_date,
            language=language,
            include_future=include_future,
        )

    def get_codes(
        self,
        from_date: str | None = None,
        to_date: str | None = None,
        select_codes: str | None = None,
        select_level: int | None = None,
        presentation_name_pattern: str | None = None,
        language: OptionalLanguage = None,
        include_future: bool | None = None,
    ) -> KlassCodes:
        """Return a KlassCodes object of the classification at a specific time or in a specific time range.

        Args:
            from_date: The start date of the time period. "YYYY-MM-DD".
            to_date: The end date of the time period. "YYYY-MM-DD".
            select_codes: Limit the result to codes matching this pattern.
                See rules: https://data.ssb.no/api/klass/v1/api-guide.html#_selectcodes.
            select_level: The level of the version to keep in the data.
            presentation_name_pattern: Used to build an alternative presentation name for the codes.
                See rules: https://data.ssb.no/api/klass/v1/api-guide.html#_presentationnamepattern.
            language: The language of the version. "nn", "nb" or "en".
            include_future: Whether to include future versions of the version.

        Returns:
            KlassCodes: A KlassCodes object of the classification at a specific time or in a specific time range.
        """
        # If not passed to method, grab these from the Classification
        if not language:
            language = self.language
        if include_future is None:
            include_future = self.include_future

        return KlassCodes(
            classification_id=self.classification_id,
            from_date=from_date,
            to_date=to_date,
            select_codes=select_codes,
            select_level=select_level,
            presentation_name_pattern=presentation_name_pattern,
            language=language,
            include_future=include_future,
        )

    def get_changes(
        self,
        from_date: str,
        to_date: str | None = None,
        language: OptionalLanguage = "nb",
        include_future: bool = False,
    ) -> pd.DataFrame:
        """Return a dataframe of the classification at a specific time or in a specific time range.

        Different from get_codes(), this method does not return all codes,
        but only what has changed since the last update or within the time range.

        Args:
            from_date: The start date of the time period. "YYYY-MM-DD".
            to_date: The end date of the time period. "YYYY-MM-DD".
            language: The language of the version. "nn", "nb" or "en".
            include_future: Whether to include future versions of the version.

        Returns:
            pd.DataFrame: A pandas DataFrame of the changes in the classification at a specific time
            (from the last time it changed) or within the specific time range.
        """
        return changes(
            classification_id=self.classification_id,
            from_date=from_date,
            to_date=to_date,
            language=language,
            include_future=include_future,
        )

    def get_latest_variant_by_name(self, variant_name: str) -> KlassVariant:
        """Attempt to get a single variant from the classification using a search string.

        Args:
            variant_name: The string to search for amongst the variant names on this classification.

        Raises:
            ValueError: If the string is not specific enough, and zero, or more than a single variant is found.

        Returns:
            KlassVariant: The single variant we found with the search string. Raises if we found no matches.
        """
        version = self.get_version()
        variants = version.variants_simple()

        results: list[str] = []
        for k, v in variants.items():
            if variant_name.lower() in v.lower():
                results.append(k)
        if len(results) > 1:
            raise ValueError(
                "Variant_name maybe not specific enough, getting multiple results."
            )
        if len(results) == 0:
            raise ValueError(
                "No result found, here are the names of the variants:\n"
                + ",\n".join(variants.values())
            )
        variant_id: str = results[0]
        return KlassVariant(variant_id)

    def join_all_variants_correspondences_on_data(
        self,
        version_id: int | None = None,
        shortname_len: int = 3,
        data_left: pd.DataFrame | None = None,
        code_col_name: str = "code",
        include_cols: list[str] | None = None,
    ) -> pd.DataFrame:
        """Join both variants and correspondences onto the main code data of the version.

        Can be quite slow, as it is doing a request to the KLASS-API for every variant and Correspondence.

        Args:
            version_id: If you want, specify the ID of the version. If None, will get the "latest" version for the classification.
            shortname_len: Amount of words from the correspondences that the new column names will be constructed from.
            data_left: A dataframe containing a column to join all the correspondences on. If None will get data from the version.
            code_col_name: The column in the data to join the code on.
            include_cols: A list of the columns from the correspondences and variants you want to include when adding to the data.
                The "targetCode" from correspondences and "parentCode" from variants is included by default, but you can add ["targetName", "name"] here to add the label of the correspondences and varians for example.

        Returns:
            pd.DataFrame: The data from the version, or from data sent to data_left, with the variants and correspondences joined on.
        """
        return self.get_version(version_id).join_all_variants_correspondences_on_data(
            shortname_len,
            data_left,
            code_col_name,
            include_cols,
        )
