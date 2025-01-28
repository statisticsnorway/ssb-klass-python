import pandas as pd
from typing_extensions import Self

from klass.utility.naming import create_shortname
from klass.classes.correspondence import KlassCorrespondence
from klass.classes.variant import KlassVariant
from klass.requests.klass_requests import version_by_id
from klass.requests.klass_types import CorrespondenceTablesType
from klass.requests.klass_types import VersionByIDType


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
        select_level (int): The level in the codelist-data to keep. Defaults to 0 (keep all).
        language (str, optional): The language of the version. Defaults to "nb", can be set to "en", or "nn".
        include_future (bool, optional): If the version should include future versions. Defaults to False.
    """

    def __init__(
        self,
        version_id: str,
        select_level: int = 0,
        language: str = "nb",
        include_future: bool = False,
    ) -> None:
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


    def get_all_variants(self) -> list[KlassVariant]:
        """Get all variants of version as a list of KlassVariants.
        
        Returns:
            list[KlassVariant]: List of the variants we found.
        
        """
        return [KlassVariant(variant_id) for variant_id in self.variants_simple()]
    

    def join_all_variants_on_data(self, shortname_len: int = 3) -> pd.DataFrame:
        """Join the variants codes onto the main codes of the version.
        
        Args:
            shortname_len: Amount of words from the variants that the new column names will be constructed from.

        Returns:
            pd.DataFrame: The joined pandas dataframe.

        Raises:
            If similar column names show up, raises and error, and suggests using more elements to create the column names.
        """
        data = self.data.copy()
        all_variants = self.get_all_variants()
        unique_codes_data = data["code"].unique()
        unique_codes_data_dict = dict(zip(unique_codes_data, unique_codes_data, strict=True))
        col_seen = list(data.columns)
        for variant in all_variants:
            mapping = unique_codes_data_dict | variant.to_dict(remove_na=True)
            shortname = create_shortname(variant, shortname_len=shortname_len)
            if shortname in col_seen:
                raise ValueError(f"Colname {shortname} already seen, increase the shortname_len?")
            data[shortname] = data["code"].map(mapping)
        return data

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

    def get_all_correspondences(self) -> list[KlassCorrespondence]:
        """Get all correspondences of version as a list of KlassCorrespondences.
        
        Returns:
            list[KlassCorrespondence]: List of the correspondences we found.
        
        """
        return [KlassCorrespondence(corr_id) for corr_id in self.correspondences_simple()]
        