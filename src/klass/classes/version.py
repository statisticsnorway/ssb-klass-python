import pandas as pd
from typing_extensions import Self

from ..requests.klass_requests import version_by_id
from ..requests.types import CorrespondenceTablesType
from ..requests.types import VersionByIDType
from .correspondence import KlassCorrespondence
from .variant import KlassVariant


class KlassVersion:
    """A version of a classification is set in time.

    For example, the ID of NUS valid in 2023 is 1954, while the ID of NUS without being time-specific is 36.

    Attributes:
        data (pd.DataFrame): The codelist of the classification-version as a pandas dataframe.
        name (str): The name of the version.
        validFrom (str): The date the version is valid from.
        validTo (str): The date the version is valid to (if any).
        lastModified (str): The date the version was last modified.
        published (list): A list of languages that the version is published in.
        introduction (str): A longer description of the version.
        contactPerson (dict): A dictionary of the contact person of the version.
        owningSection (str): The name of the section that owns the version.
        legalBase (str): The basis in law for the classification.
        publications (str): Where the classification is published (URL).
        derivedFrom (str): Notes on where the classification was derived from.
        correspondenceTables (list): A list of correspondence-tables of the version.

    Args:
        version_id (str): The ID of the version.
        select_level (int, optional): The level in the codelist-data to keep. Defaults to 0.
        language (str, optional): The language of the version. Defaults to "nb", can be set to "en", or "nn".
        include_future (bool, optional): If the version should include future versions. Defaults to False.
    """

    def __init__(
        self,
        version_id: str,
        select_level: int = 0,
        language: str = "nb",
        include_future: bool = False,
    ):
        """Set up the object with data from the KLASS-API."""
        self.version_id = version_id
        self.select_level = select_level
        self.language = language.lower()
        self.include_future = include_future

        result: VersionByIDType = version_by_id(
            version_id,
            language=language,
            include_future=include_future,
        )
        self.name: str = result["name"]
        self.validFrom: str = result["validFrom"]
        if "validTo" in result:
            self.validTo: str = result["validTo"]
        self.lastModified: str = result["lastModified"]
        self.published: list[str] = result["published"]
        self.introduction: str = result["introduction"]
        self.contactPerson: dict[str, str] = result["contactPerson"]
        self.owningSection: str = result["owningSection"]
        if "legalBase" in result:
            self.legalBase: str = result["legalBase"]
        if "publications" in result:
            self.publications: str = result["publications"]
        if "derivedFrom" in result:
            self.derivedFrom: str = result["derivedFrom"]
        self.correspondenceTables: list[CorrespondenceTablesType] = result[
            "correspondenceTables"
        ]
        if "classificationVariants" in result:
            self.classificationVariants: list[CorrespondenceTablesType] = result[
                "classificationVariants"
            ]
        self.changelogs: list[dict[str, str]] = result["changelogs"]
        self.levels: list[dict[str, int | str]] = result["levels"]
        self.classificationItems: list[dict[str, str | None]] = result[
            "classificationItems"
        ]
        self.links: dict[str, dict[str, str]] = result["_links"]

        self.get_classification_codes()

    def __repr__(self) -> str:
        """Get a string representation of how to recreate the object, including its set parameters."""
        result = f'KlassVersion(version_id="{self.version_id}", '
        if self.select_level:
            result += f"select_level={self.select_level}, "
        if self.language != "nb":
            result += f'language="{self.language}", '
        if self.include_future:
            result += f"include_future={self.include_future}"
        result += ")"
        return result

    def __str__(self) -> str:
        """Print a human-readable string of the object, includes many of its attributes or their sizes."""
        if hasattr(self, "classificationVariants"):
            number_variants = f"\n\tNumber of classification variants: {len(self.classificationVariants)}"
        else:
            number_variants = ""
        contact = "Contact Person:\n"
        for k, v in self.contactPerson.items():
            contact += f"\t{k}: {v}\n"

        result = f"""Version {self.version_id}: {self.name}
        Owning Section: {self.owningSection}
        Valid: {self.validFrom} ->"""
        if hasattr(self, "validTo"):
            result += f"{self.validTo}"
        result += (
            f"""\nLast modified: {self.lastModified}
        {contact}

        Number of correspondences: {len(self.correspondenceTables)}"""
            + number_variants
            + f"""
        Number of classification items: {len(self.classificationItems)}
        Number of levels: {len(self.levels)}


{self.introduction}
        """
        )
        return result

    def get_classification_codes(self, select_level: int = 0) -> Self:
        """Get the codelists of the version. Inserts the result into the KlassVersions .data attribute, instead of returning it.

        Run as a part of the class initialization.

        Args:
            select_level (int): The level of the version to keep in the data. Setting to 0 keeps all levels.

        Returns:
            self (KlassVersion): Returns self to make the method more easily chainable.
        """
        if not select_level and self.select_level:
            select_level = self.select_level
        data = pd.json_normalize(self.classificationItems)
        level_map = {
            str(item["levelNumber"]): item["levelName"] for item in self.levels
        }
        data.insert(
            data.columns.to_list().index("level") + 1,
            "levelName",
            data["level"].astype(str).map(level_map),
        )
        if select_level:
            data = data[data["level"].astype(str) == str(select_level)]
        self.data = data
        return self

    def variants_simple(self) -> dict[str, str]:
        """Get a simplifed dictionary of the variants, ids as keys, names as values."""
        return {
            v["_links"]["self"]["href"].split("/")[-1]: v["name"]
            for v in self.classificationVariants
        }

    @staticmethod
    def get_variant(
        variant_id: str, select_level: int = 0, language: str = "nb"
    ) -> KlassVariant:
        """Get a specific variant.

        Args:
            variant_id (str): The ID of the variant.
            select_level (int): The level of the variant to keep in the data. Setting to 0 keeps all levels.
            language (str): The language of the variant.

        Returns:
            KlassVariant: A variant object with the specified ID and language.
        """
        return KlassVariant(variant_id, select_level, language)

    def correspondences_simple(self) -> dict[str, dict[str, str]]:
        """Get a simple dictionary of the correspondences.

        With the IDs as keys.

        Returns:
            dict: A nested dictionary of the available correspondences.
        """
        tables = {}
        for tab in self.correspondenceTables:
            links: dict[str, dict[str, str]] = tab["_links"]
            corr_link: str = links["self"]["href"]
            corr_id: str = corr_link.split("/")[-1]
            tables[corr_id] = {
                "name": tab["name"],
                "source": tab["source"],
                "source_id": tab["sourceId"],
                "target": tab["target"],
                "target_id": tab["targetId"],
            }
        return tables

    @staticmethod
    def get_correspondence(
        correspondence_id: str = "",
        source_classification_id: str = "",
        target_classification_id: str = "",
        from_date: str = "",
        to_date: str = "",
        contain_quarter: int = 0,
        language: str = "nb",
        include_future: bool = False,
    ) -> KlassCorrespondence:
        """Get a specific correspondence.

        Args:
            correspondence_id (str): The ID of the correspondence.
            source_classification_id (str): The ID of the source classification.
            target_classification_id (str): The ID of the target classification.
            from_date (str): The start date of the correspondence.
            to_date (str): The end date of the correspondence.
            contain_quarter (int): The number of quarters the correspondence should contain.
            language (str): The language of the correspondence. "nb", "nn" or "en".
            include_future (bool): If the correspondence should include future correspondences.

        Returns:
            KlassCorrespondence: A correspondence object with the specified ID, language, and dates.
        """
        return KlassCorrespondence(
            correspondence_id=correspondence_id,
            source_classification_id=source_classification_id,
            target_classification_id=target_classification_id,
            from_date=from_date,
            to_date=to_date,
            contain_quarter=contain_quarter,
            language=language,
            include_future=include_future,
        )
