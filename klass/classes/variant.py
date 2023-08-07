import pandas as pd

from ..requests.klass_requests import variant, variant_at, variants_by_id


class KlassVariant:
    def __init__(
        self,
        variant_id: str,
        select_level: int = 0,
        language: str = "nb",
    ):
        self.variant_id = variant_id
        self.select_level = select_level
        self.language = language
        for key, value in variants_by_id(self.variant_id, self.language).items():
            setattr(self, key, value)
        self.get_classification_codes()

    def get_classification_codes(self, select_level: int = 0) -> pd.DataFrame:
        df = pd.json_normalize(self.classificationItems)
        if not select_level:
            if self.select_level:
                select_level = self.select_level
        if select_level:
            return df[df["level"] == str(select_level)]
        self.data = df

    def __repr__(self):
        result = f"KlassVariant(variant_id={self.variant_id}, "
        if self.select_level:
            result += f"select_level={self.select_level}, "
        if self.language != "nb":
            result += f"language={self.language}"
        result += ")"
        return result

    def __str__(self):
        result = f"This is a Klass Variant with the ID of {self.variant_id}."
        result += f"\nPreview of the .data:\n{self.data[self.data.columns[:5]].head(5)}"
        return result


class KlassVariantSearch:
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
        self.classification_id = classification_id
        self.variant_name = variant_name
        self.from_date = from_date
        self.to_date = to_date
        self.select_codes = (select_codes,)
        self.select_level = (select_level,)
        self.presentation_name_pattern = presentation_name_pattern
        self.language = language
        self.include_future = include_future

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

    def __repr__(self):
        result = f'KlassVariantSearch(classification_id="{self.classification_id}", '
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

    def __str__(self):
        result = f"A search for variants on classification ID {self.classification_id} on the name {self.variant_name}.\n"
        result += f"From the date {self.from_date}"
        if self.to_date:
            result += f", to the date {self.to_date}"
        result += (
            f".\nPreview of the .data:\n{self.data[self.data.columns[:5]].head(5)}"
        )
        return result

    @staticmethod
    def get_variant(
        variant_id: str,
        language: str = "nb",
    ) -> KlassVariant:
        return KlassVariant(
            variant_id=variant_id,
            language=language,
        )
