import pandas as pd

from ..requests.klass_requests import variant, variant_at, variants_by_id


class KlassVariant:
    """In Klass a Variant is a different way of aggregating an existing codelist.
    It does not have to be extensive (all filled out), but can for example
    redefine upper levels, for some lower-level codes.

    For example:
    "Study points for vocational education programmes" is a Version (ID 1959)
    for the Classification of Education (NUS, ID 36).
    It sets a new upper level of codes (amount of study points),
    for a set of lower-level existing codes (NUS codes, level 5).

    Parameters
    ----------
    variant_id : str
        The variant_id of the variant.
        For example: '1959'
    select_level : int
        The level of the dataset to keep
        For example: 5
    language : str
        The language of the variant to select.
        For example: 'nb'

    Attributes
    ----------
    data : pd.DataFrame
        The classificationItems as a pandas dataframe. Usually what you're after?
    variant_id : str
        The variant_id of the variant.
        For example: '36'
    select_level : int
        The level of the dataset to keep
        For example: 0
    language : str
        The language of the variant to select.
        For example: 'nb'
    classificationItems : list
        The json returned from the API, which is converted to a pandas dataframe under
        the .data attribute on initialization.
    """
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

    def get_classification_codes(self, select_level: int = 0) -> None:
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


class KlassVariantSearchByName:
    """Looks up a Variant based on the owning Classifications ID and the start of the Variants name.
    The name is put into a URL-parameter, so it might be sensitive to special characters, 
    if the name you are trying isnt working, try keeping less of it, but keep the start of the name.

    There might be a bug (2023), where you can get duplicate rows from the API on this,
    so if you use this class, make sure to check for duplicates before moving on.

    In Klass a Variant is a different way of aggregating an existing codelist.
    It does not have to be extensive (all filled out), but can for example
    redefine upper levels, for some lower-level codes.

    Parameters
    ----------
    classification_id : str
        The classification id.
    variant_name : str
        The start of the variant name.
    from_date : str
        The start of the date range.
    to_date : str
        The end of the date range.
    select_codes : str
        Limit the result to codes matching this pattern. See rules: https://data.ssb.no/api/klass/v1/api-guide.html#_selectcodes
    select_level : str
        The level of codes to keep in the dataset
    presentation_name_pattern : str
        Used to build an alternative presentation name for the codes. See rules: https://data.ssb.no/api/klass/v1/api-guide.html#_presentationnamepattern
    language : str 
        Language of the names, select "en", "nb" or "nn".
    include_future : bool
        Whether to include future codes. Defaults to False.


    Attributes
    ----------
    data : pd.DataFrame
        The codelists from the Variant as a pandas dataframe. Usually what you're after?
    classification_id : str
        The classification id.
    variant_name : str
        The start of the variant name.
    from_date : str
        The start of the date range.
    to_date : str
        The end of the date range.
    select_codes : str
        Limit the result to codes matching this pattern. See rules: https://data.ssb.no/api/klass/v1/api-guide.html#_selectcodes
    select_level : str
        The level of codes to keep in the dataset
    presentation_name_pattern : str
        Used to build an alternative presentation name for the codes. See rules: https://data.ssb.no/api/klass/v1/api-guide.html#_presentationnamepattern
    language : str 
        Language of the names, select "en", "nb" or "nn".
    include_future : bool
        Whether to include future codes. Defaults to False.

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
        self.classification_id = classification_id
        self.variant_name = variant_name
        self.from_date = from_date
        self.to_date = to_date
        self.select_codes = select_codes
        self.select_level = select_level
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

    def __str__(self):
        result = f'A search for variants on classification ID "{self.classification_id}" on the name "{self.variant_name}".\n'
        result += f"From the date {self.from_date}"
        if self.to_date:
            result += f", to the date {self.to_date}"
        result += (
            f".\nPreview of the .data:\n{self.data[self.data.columns[:5]].head(5)}"
        )
        return result
