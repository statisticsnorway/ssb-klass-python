from collections import defaultdict
from datetime import datetime

import pandas as pd
from typing_extensions import Self

from klass.requests.klass_requests import codes
from klass.requests.klass_requests import codes_at


class KlassCodes:
    r"""Get codes from Klass.

    The codelist is owned by the Classification through a Version, and will be valid for a time period.

    Attributes:
        data (pd.DataFrame): The pandas DataFrame of the codes.
        classification_id (str): The classification ID.
        from_date (str): The start date of the time period. "YYYY-MM-DD".
        to_date (str): The end date of the time period. "YYYY-MM-DD".

    Args:
        classification_id (str): The classification ID.
        from_date (str): The start date of the time period. "YYYY-MM-DD".
        to_date (str): The end date of the time period. "YYYY-MM-DD".
        select_codes (str): A list of codes to be selected.
        select_level (str): A list of levels to be selected.
        presentation_name_pattern (str): A pattern for filtering the code names.
        language (str): The language of the code names. Defaults to "nb".
        include_future (bool): Whether to include future codes. Defaults to False.

    Raises:
        ValueError: If from_date or to_date is not a valid date or date-string YYYY-MM-DD.
        ValueError: If select_codes contains anything except numbers and the special characters "*" (star) or "-" (dash).
        ValueError: If select_level is anything except a whole number.
        ValueError: If presentation_name_pattern is not a valid pattern.
        ValueError: If language is not "nb", "nn" or "en".
        ValueError: If include_future is not a bool.
    """

    def __init__(
        self,
        classification_id: str = "",
        from_date: str = "",
        to_date: str = "",
        select_codes: str = "",
        select_level: str = "",
        presentation_name_pattern: str = "",
        language: str = "nb",
        include_future: bool = False,
    ):
        """Get the data from the KLASS-api belonging to the code-list."""
        self.classification_id = classification_id
        if not from_date:
            from_date = datetime.now().strftime("%Y-%m-%d")
        self.from_date = from_date
        self.to_date = to_date
        self.select_codes = select_codes
        self.select_level = select_level
        self.presentation_name_pattern = presentation_name_pattern
        self.language = language
        self.include_future = include_future
        self.get_codes()

    def __repr__(self) -> str:
        """Return a copy-pasteable string to recreate the object."""
        result = f"KlassCodes(classification_id={self.classification_id}, "
        result += f"from_date={self.from_date}, "
        if self.to_date:
            result += f"to_date={self.to_date}, "
        if self.language != "nb":
            result += f"language={self.language}, "
        if self.include_future:
            result += f"include_future={self.include_future}, "
        result += ")"
        return result

    def __str__(self) -> str:
        """Print a readable string of the codelist, including some of its attributes."""
        unique_levels = ", ".join(self.data["level"].unique())
        some_names = ", \n\t- ".join(
            self.data[self.data["name"].notna()]["name"].value_counts().iloc[:5].index
        )
        result = f"""Codelist for classification: {self.classification_id}
        From date: {self.from_date}"""
        if self.to_date:
            result += f"""To date: {self.to_date}"""
        result += f"""

        Unique levels: {unique_levels}
        Some code names:
        - {some_names}

        Take a look at the .data attribute for the DataFrame containing the codes.
        """
        return result

    def change_dates(
        self,
        from_date: str = "",
        to_date: str = "",
        include_future: bool | None = None,
    ) -> Self:
        """Change the dates of the codelist and get the data again based on new dates.

        Args:
            from_date (str): The start date of the time period. "YYYY-MM-DD".
            to_date (str): The end date of the time period. "YYYY-MM-DD".
            include_future (bool): Whether to include future codes.

        Returns:
            self (KlassSearchFamilies): Returns self to make the method more easily chainable.
        """
        if not from_date:
            from_date = datetime.now().strftime("%Y-%m-%d")
        if include_future is not None:
            self.include_future = include_future
        self.from_date = from_date
        self.to_date = to_date
        self.get_codes()
        return self

    def get_codes(self, raise_on_empty_data: bool = True) -> Self:
        """Retrieve codes from the classification specified by self.classification_id at a specific time.

        If self.to_date is not None, codes will be retrieved from the date range specified
        by self.from_date and self.to_date. Otherwise, codes will be retrieved only for
        the date specified by self.from_date.

        Args:
            raise_on_empty_data (bool): Whether to raise an error if the returned dataframe is empty. Defaults to True.

        Returns:
            self (KlassSearchFamilies): Returns self to make the method more easily chainable.

        Raises:
            ValueError: If the returned dataframe is empty, there is probably something too narrow in the parameters.
        """
        if self.to_date:
            self.data = codes(
                classification_id=self.classification_id,
                from_date=self.from_date,
                to_date=self.to_date,
                select_codes=self.select_codes,
                select_level=self.select_level,
                presentation_name_pattern=self.presentation_name_pattern,
                language=self.language,
                include_future=self.include_future,
            )
        else:
            self.data = codes_at(
                classification_id=self.classification_id,
                date=self.from_date,
                select_codes=self.select_codes,
                select_level=self.select_level,
                presentation_name_pattern=self.presentation_name_pattern,
                language=self.language,
                include_future=self.include_future,
            )
        if len(self.data) == 0 and raise_on_empty_data:
            raise ValueError(
                "Empty data, no codes found for the specified parameters. Maybe your select_codes or select_level is too narrow?"
            )
        return self

    def to_dict(
        self,
        key: str = "code",
        value: str = "",  # default is "name" if not set
        other: str = "",
    ) -> dict[str, str] | defaultdict[str, str]:
        """Extract two columns from the data, turning them into a dict.

        If you specify a value for "other", returns a defaultdict instead.

        Args:
            key (str): The name of the column with the values you want as keys.
            value (str): The name of the column with the values you want as values in your dict.
            other (str): If key is missing from dict, return this value instead, if you specify an OTHER-value.

        Returns:
            dict | defaultdict: The extracted columns as a dict or defaultdict.
        """
        if not value:
            # If you bothered specifying a pattern, we assume you want it
            if self.presentation_name_pattern:
                value = "presentationName"
            else:
                value = "name"
        mapping = dict(zip(self.data[key], self.data[value]))
        if other:
            mapping = defaultdict(lambda: other, mapping)
        return mapping

    def pivot_level(self, keep: list[str] | None = None) -> pd.DataFrame:
        """Pivot levels into separate columns and number columns based on levels as suffixes.

        Joining children codes onto their parent codes.
        For example, instead of "code", gives you "code_1", "code_2" etc.

        First envisioned by @mfmssb

        Args:
            keep (list[str]): The start of the names of the columns you want to keep when done.
                Default is ["code", "name"], but other possibilities are "presentationName",
                "level", "shortName", "validTo", "validFrom", and "notes".

        Returns:
            pd.DataFrame: The resulting pandas DataFrame.
        """
        if keep is None:
            keep = ["code", "name"]
        df = pd.DataFrame()
        lev_previous = 1
        for lev in self.data["level"].unique():
            temp = self.data[self.data["level"] == lev].copy()
            temp.columns = [f"{c}_{lev}" for c in temp.columns]
            if len(df):
                df = df.merge(
                    temp,
                    how="right",
                    left_on=f"code_{lev_previous}",
                    right_on=f"parentCode_{lev}",
                )
            else:
                df = temp
            lev_previous = lev
        keep_cols = []
        for col in df.columns:
            for keep_col in keep:
                if col.lower().startswith(keep_col.lower()):
                    keep_cols += [col]
        df = df[keep_cols]
        return df
