import pandas as pd

from ..requests.klass_requests import variant, variant_at, variants_by_id


class KlassVariant:
    def __init__(
        self,
        variant_id: str,
        language: str = "nb",
    ):
        self.variant_id = variant_id
        self.language = language
        for key, value in variants_by_id(self.variant_id, self.language).items():
            setattr(self, key, value)

    def get_classification_codes(self, select_level: int = 0) -> pd.DataFrame:
        df = pd.json_normalize(self.classificationItems)
        if select_level:
            return df[df["level"] == str(select_level)]
        return df


class KlassVariantsSearch:
    def __init__(
        self,
        classification_id: str,
        variant_name: str,
        from_date: str,
        to_date: str = "",
        presentation_name_pattern: str = "",
        language: str = "nb",
        include_future: bool = False,
    ):
        self.classification_id = classification_id
        self.variant_name = variant_name
        self.from_date = from_date
        self.to_date = to_date
        self.presentation_name_pattern = presentation_name_pattern
        self.language = language
        self.include_future = include_future

        if self.to_date:
            result = variant(
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
            result = variant_at(
                classification_id=self.classification_id,
                variant_name=self.variant_name,
                date=self.from_date,
                select_codes=self.select_codes,
                select_level=self.select_level,
                presentation_name_pattern=self.presentation_name_pattern,
                language=self.language,
                include_future=self.include_future,
            )
        for key, value in result.items():
            setattr(self, key, value)

        @staticmethod
        def get_variant(
            variant_id: str,
            language: str = "nb",
        ) -> KlassVariant:
            return KlassVariant(
                variant_id=variant_id,
                language=language,
            )
