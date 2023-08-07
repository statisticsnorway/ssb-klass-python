import pandas as pd

from ..requests.klass_requests import version_by_id
from .correspondance import KlassCorrespondance
from .variant import KlassVariant


class KlassVersion:
    """A version of a classification, is set in time.
    For example the ID of NUS valid in 2023 is 1954, while the ID of NUS without being time-specific is 36.

    Parameters
    ----------
    version_id : str
        The id of the version.
    select_level : int, optional
        The level in the codelist-data to keep. Defaults to 0.
    language : str, optional
        The language of the version. Defaults to "nb", can be set to "en", or "nn".
    include_future : bool, optional
        If the version should include future versions. Defaults to False.

    Attributes
    ----------
    data : pd.DataFrame
        The codelist of the classification-version as a pandas dataframe
    name : str
        The name of the version.
    validFrom : str
        The date the version is valid from.
    validTo : str
        The date the version is valid to (if any).
    lastModified : str
        The date the version was last modified.
    published: list
        A list of languages that the version is published in.
    introduction : str
        A longer description of the version.
    contactPerson : dict
        A dictionary of the contact person of the version.
    owningSection : str
        The name of the section that owns the version.
    legalBase: str
        The basis in law for the classification.
    publications : str (url)
        Where the classification is published.
    derivedFrom : str
        Notes on where the classification was derived from.
    correspondenceTables : list
        A list of correspondance-tables of the version.
    """
    def __init__(
        self,
        version_id: str,
        select_level: int = 0,
        language: str = "nb",
        include_future: bool = False,
    ):
        self.version_id = version_id
        self.select_level = select_level
        self.language = language.lower()
        self.include_future = include_future
        for key, value in version_by_id(
            version_id,
            language=language,
            include_future=include_future,
        ).items():
            setattr(self, key, value)
        self.get_classification_codes()

    def __repr__(self):
        result = f'KlassVersion(version_id="{self.version_id}", '
        if self.select_level:
            result += f"select_level={self.select_level}, "
        if self.language != "nb":
            result += f'language="{self.language}", '
        if self.include_future:
            result += f"include_future={self.include_future}"
        result += ")"
        return result

    def __str__(self):
        contact = "Contact Person:\n"
        for k, v in self.contactPerson.items():
            contact += f"\t{k}: {v}\n"

        result = f"""Version {self.version_id}: {self.name}
        Owning Section: {self.owningSection}
        Valid: {self.validFrom} ->"""
        if hasattr(self, "validTo"):
            result += f"{self.validTo}"
        result += f"""\nLast modified: {self.lastModified}
        {contact}

        Number of correspondances: {len(self.correspondenceTables)}
        Number of classification variants: {len(self.classificationVariants)}
        Number of classification items: {len(self.classificationItems)}
        Number of levels: {len(self.levels)}


{self.introduction}
        """
        return result

    def get_classification_codes(self, select_level: int = 0) -> None:
        if not select_level:
            if self.select_level:
                select_level = self.select_level
        data = pd.json_normalize(self.classificationItems)
        level_map = {
            str(item["levelNumber"]): item["levelName"] for item in self.levels
        }
        level_map_reverse = {v: k for k, v in level_map.items()}
        data.insert(
            data.columns.to_list().index("level") + 1,
            "levelName",
            data["level"].astype(str).map(level_map),
        )
        if not str(select_level).isdigit():
            select_level = level_map_reverse[select_level]
        if select_level:
            data = data[data["level"].astype(str) == str(select_level)]
        self.data = data

    def variants_simple(self) -> dict:
        return {
            v["_links"]["self"]["href"].split("/")[-1]: v["name"]
            for v in self.classificationVariants
        }

    @staticmethod
    def get_variant(
        variant_id: str, select_level: int = 0, language: str = "nb"
    ) -> KlassVariant:
        return KlassVariant(variant_id, select_level, language)

    def correspondances_simple(self) -> dict:
        tables = {}
        for tab in self.correspondenceTables:
            corr_id = tab["_links"]["self"]["href"].split("/")[-1]
            tables[corr_id] = {
                "name": tab["name"],
                "source": tab["source"],
                "source_id": tab["sourceId"],
                "target": tab["target"],
                "target_id": tab["targetId"],
            }
        return tables

    @staticmethod
    def get_correspondance(
        correspondance_id: str = "",
        source_classification_id: str = "",
        target_classification_id: str = "",
        from_date: str = "",
        to_date: str = "",
        contain_quarter: int = 0,
        language: str = "nb",
        include_future: bool = False,
    ) -> KlassCorrespondance:
        return KlassCorrespondance(
            correspondance_id=correspondance_id,
            source_classification_id=source_classification_id,
            target_classification_id=target_classification_id,
            from_date=from_date,
            to_date=to_date,
            contain_quarter=contain_quarter,
            language=language,
            include_future=include_future,
        )
