import pandas as pd

from ..requests.klass_requests import changes, classification_by_id
from .codes import KlassCodes
from .correspondance import KlassCorrespondance
from .variant import KlassVariant
from .version import KlassVersion


class KlassClassification:
    def __init__(
        self, classification_id: str, language: str = "nb", include_future: bool = False
    ):
        self.classification_id = classification_id
        self.language = language
        self.include_future = include_future

        for key, value in classification_by_id(
            classification_id, language=language, include_future=include_future
        ).items():
            setattr(self, key, value)

        version_replace = []
        for ver in self.versions:
            version_replace.append(
                {"version_id": int(ver["_links"]["self"]["href"].split("/")[-1]), **ver}
            )
        self.versions = version_replace

    def __str__(self):
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

    def __repr__(self):
        result = f"KlassClassification(classification_id='{self.classification_id}', "
        if self.language != "nb":
            result += f"language='{self.language}', "
        if self.include_future:
            result += "include_future=True, "
        result += ")"
        return result

    @staticmethod
    def get_version(version_id) -> KlassVersion:
        return KlassVersion(version_id)

    def get_variants() -> list[KlassVariant]:
        pass

    def get_variant() -> KlassVariant:
        pass

    def get_correspondance_to(
        self,
        target_classification_id: str,
        from_date: str,
        to_date: str = "",
        language: str = "",
        include_future: bool = None,
    ) -> KlassCorrespondance:
        if language == "":
            language = self.language
        if include_future is None:
            include_future = self.include_future
        return KlassCorrespondance(
            source_classification_id=self.classification_id,
            target_classification_id=target_classification_id,
            from_date=from_date,
            to_date=to_date,
            language=language,
            include_future=include_future,
        )

    def get_codes(
        self,
        from_date: str = "",
        to_date: str = "",
        select_codes: str = "",
        select_level: str = "",
        presentation_name_pattern: str = "",
        language: str = "",
        include_future: bool = None,
    ) -> KlassCodes:
        # If not passed to method, grab these from the Classification
        if language == "":
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
        to_date: str = "",
        language: str = "nb",
        include_future: bool = False,
    ) -> pd.DataFrame:
        return changes(
            classification_id=self.classification_id,
            from_date=from_date,
            to_date=from_date,
            language=language,
            include_future=include_future,
        )
