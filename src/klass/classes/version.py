import pandas as pd
from typing_extensions import Self
from typing_extensions import overload

from ..requests.klass_requests import version_by_id
from ..requests.klass_types import CorrespondenceTablesType
from ..requests.klass_types import Language
from ..requests.klass_types import VersionByIDType
from ..utility.naming import create_shortname
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
        version_id: The ID of the version.
        select_level: The level in the codelist-data to keep. Defaults to 0 (keep all).
        language: The language of the version. Defaults to "nb", can be set to "en", or "nn".
        include_future: If the version should include future versions. Defaults to False.
    """

    def __init__(
        self,
        version_id: str | int,
        select_level: int | None = None,
        language: Language = "nb",
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

    def get_classification_codes(self, select_level: int | None = None) -> Self:
        """Get the codelists of the version. Inserts the result into the KlassVersions .data attribute, instead of returning it.

        Run as a part of the class initialization.

        Args:
            select_level: The level of the version to keep in the data. Setting to 0 keeps all levels.

        Returns:
            self (KlassVersion): Returns self to make the method more easily chainable.
        """
        select_level = select_level if select_level else self.select_level
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

    def get_variant(
        self,
        variant_id: str | int | None = None,
        search_term: str = "",
        select_level: int | None = None,
        language: Language = "nb",
    ) -> KlassVariant:
        """Get a specific variant.

        Args:
            variant_id: The ID of the variant.
            search_term: Search term to look for in the name of the klass variant you want to look for.
            select_level: The level of the variant to keep in the data. Setting to 0 keeps all levels.
            language: The language of the variant.

        Returns:
            KlassVariant: A variant object with the specified ID and language.

        Raises:
            ValueError: If you are missing an identifier, or you send somethign else than a str as the search_term, or if we find more than one match for the search_term.

        """
        if variant_id is None and not search_term:
            raise ValueError("You need to specify either variant_id or a search-term.")
        if variant_id is not None:
            return KlassVariant(variant_id, select_level, language)
        if not isinstance(search_term, str):
            raise ValueError(
                "Hey, did you notice the new search_term parameter? Send in select_level as a keyword argument instead..."
            )

        found_variants = {
            k: v
            for k, v in self.variants_simple().items()
            if search_term.lower() in v.lower()
        }
        if len(found_variants) != 1:
            err_msg = f"When searching for a variant that matches your search, we did not find a single match. If you got multiple matches, be more specific in your search term: {list(found_variants.values())}"
            raise ValueError(err_msg)
        return KlassVariant(next(iter(found_variants.keys())), select_level, language)

    def get_all_variants(self) -> list[KlassVariant]:
        """Get all variants of version as a list of KlassVariants.

        Can be quite slow, as it is doing a request to the KLASS-API for every variant.

        Returns:
            list[KlassVariant]: List of the variants we found.

        """
        return [KlassVariant(variant_id) for variant_id in self.variants_simple()]

    def join_all_variants_on_data(
        self,
        shortname_len: int = 3,
        data_left: pd.DataFrame | None = None,
        code_col_name: str = "code",
        include_cols: list[str] | None = None,
    ) -> pd.DataFrame:
        """Join the variants codes onto the main codes of the version.

        Can be quite slow, as it is doing a request to the KLASS-API for every variant.

        Args:
            shortname_len: Amount of words from the variants that the new column names will be constructed from.
            data_left: A dataframe containing a column to join all the variants on.
            code_col_name: The column in the data to join the code on.
            include_cols: A list of the columns from the variants you want to include when adding to the data.
                The "parentCode" is included by default, but you can add ["name"] here to add the label of the variant code.

        Returns:
            pd.DataFrame: The joined pandas dataframe.

        Raises:
            ValueError: If similar column names show up, raises and error, and suggests using more elements to create the column names.
        """
        if isinstance(data_left, pd.DataFrame):
            data = data_left.copy()
        else:
            data = self.data.copy()

        # Remove all empty columns
        data.isna().all()
        all_variants = self.get_all_variants()
        col_seen = list(data.columns)
        for variant in all_variants:
            shortname = create_shortname(variant, shortname_len=shortname_len)
            if shortname in col_seen:
                raise ValueError(
                    f"Colname {shortname} already seen, increase the shortname_len?"
                )
            else:
                col_seen += [shortname]

            data[shortname] = data[code_col_name].map(variant.to_dict(remove_na=True))
            if include_cols:
                for col in include_cols:
                    if col in variant.data.columns:
                        data[f"{shortname}_{col}"] = data[code_col_name].map(
                            variant.to_dict(value=col, remove_na=True)
                        )
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
    @overload
    def get_correspondence(
        correspondence_id: str | int = ...,
        source_classification_id: None = ...,
        target_classification_id: None = ...,
        from_date: None = ...,
        to_date: None = ...,
        contain_quarter: int = ...,
        language: Language = ...,
        include_future: bool = ...,
    ) -> KlassCorrespondence: ...

    @staticmethod
    @overload
    def get_correspondence(
        correspondence_id: None = ...,
        source_classification_id: str | int = ...,
        target_classification_id: str | int = ...,
        from_date: str = ...,
        to_date: str | None = ...,
        contain_quarter: int = ...,
        language: Language = ...,
        include_future: bool = ...,
    ) -> KlassCorrespondence: ...

    @staticmethod
    def get_correspondence(
        correspondence_id: str | int | None = None,
        source_classification_id: str | int | None = None,
        target_classification_id: str | int | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        contain_quarter: int = 0,
        language: Language = "nb",
        include_future: bool = False,
    ) -> KlassCorrespondence:
        """Get a specific correspondence.

        Args:
            correspondence_id: The ID of the correspondence.
            source_classification_id: The ID of the source classification.
            target_classification_id: The ID of the target classification.
            from_date: The start date of the correspondence.
            to_date: The end date of the correspondence.
            contain_quarter: The number of quarters the correspondence should contain.
            language: The language of the correspondence. "nb", "nn" or "en".
            include_future: If the correspondence should include future correspondences.

        Returns:
            KlassCorrespondence: A correspondence object with the specified ID, language, and dates.
        """
        return KlassCorrespondence(
            correspondence_id=correspondence_id,  # type: ignore [arg-type]
            source_classification_id=source_classification_id,  # type: ignore [arg-type]
            target_classification_id=target_classification_id,  # type: ignore [arg-type]
            from_date=from_date,  # type: ignore [arg-type]
            to_date=to_date,  # type: ignore [arg-type]
            contain_quarter=contain_quarter,
            language=language,
            include_future=include_future,
        )  # type: ignore [misc]

    def get_all_correspondences(self) -> list[KlassCorrespondence]:
        """Get all correspondences of version as a list of KlassCorrespondences.

        Returns:
            list[KlassCorrespondence]: List of the correspondences we found.

        """
        return [
            KlassCorrespondence(correspondence_id)
            for correspondence_id in self.correspondences_simple()
        ]

    def join_all_correspondences_on_data(
        self,
        shortname_len: int = 3,
        data_left: pd.DataFrame | None = None,
        code_col_name: str = "code",
        include_cols: list[str] | None = None,
    ) -> pd.DataFrame:
        """Join the correspondences codes onto the main codes of the version.

        Can be quite slow, as it is doing a request to the KLASS-API for every correspondence.

        Args:
            shortname_len: Amount of words from the correspondences that the new column names will be constructed from.
            data_left: A dataframe containing a column to join all the correspondences on.
            code_col_name: The column in the data to join the code on.
            include_cols: A list of the columns from the correspondences you want to include when adding to the data.
                The "targetCode" is included by default, but you can add ["targetName"] here to add the label of the correspondence code for example.

        Returns:
            pd.DataFrame: The joined pandas dataframe.

        Raises:
            ValueError: If similar column names show up, raises and error, and suggests using more elements to create the column names.
        """
        if isinstance(data_left, pd.DataFrame):
            data = data_left.copy()
        else:
            data = self.data.copy()
        # Remove all empty columns
        data.isna().all()
        all_correspondences = self.get_all_correspondences()
        col_seen = list(data.columns)
        for correspondence in all_correspondences:
            shortname = create_shortname(correspondence, shortname_len=shortname_len)
            if shortname in col_seen:
                raise ValueError(
                    f"Colname {shortname} already seen, increase the shortname_len?"
                )
            else:
                col_seen += [shortname]
            data[shortname] = data[code_col_name].map(
                correspondence.to_dict(remove_na=True)
            )
            if include_cols:
                for col in include_cols:
                    if col in correspondence.data.columns:
                        data[f"{shortname}_{col}"] = data[code_col_name].map(
                            correspondence.to_dict(value=col, remove_na=True)
                        )

        return data

    def join_all_variants_correspondences_on_data(
        self,
        shortname_len: int = 3,
        data_left: pd.DataFrame | None = None,
        code_col_name: str = "code",
        include_cols: list[str] | None = None,
    ) -> pd.DataFrame:
        """Join both variants and correspondences onto the main code data of the version.

        Can be quite slow, as it is doing a request to the KLASS-API for every correspondence and variant.

        Args:
            shortname_len: Amount of words from the correspondences that the new column names will be constructed from.
            data_left: A dataframe containing a column to join all the correspondences on. If None will get data from the version.
            code_col_name: The column in the data to join the code on.
            include_cols: A list of the columns from the correspondences and variants you want to include when adding to the data.
                The "targetCode" from correspondences and "parentCode" from variants is included by default, but you can add ["targetName", "name"] here to add the label of the correspondences and varians for example.

        Returns:
            pd.DataFrame: The data from the version, or from data sent to data_left, with the variants and correspondences joined on.
        """
        data = self.join_all_variants_on_data(
            shortname_len, data_left, code_col_name, include_cols
        )
        return self.join_all_correspondences_on_data(
            shortname_len, data, code_col_name, include_cols
        )
