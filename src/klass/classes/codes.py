from collections import defaultdict
from datetime import datetime

import pandas as pd

from ..requests.klass_requests import codes
from ..requests.klass_requests import codes_at


class KlassCodes:
    """Gets codes from Klass.

    The codelist is owned by the Classification through a Version, and will be valid for a time-period.

    Parameters
    ----------
    classification_id : str
        The classification id.
    from_date : str
        The start date of the time period.
    to_date : str
        The end date of the time period.
    select_codes : str
        A list of codes to be selected.
    select_level : str
        A list of levels to be selected.
    presentation_name_pattern : str
        A pattern for filtering the code names.
    language : str
        The language of the code names. Defaults to "nb".
    include_future : bool
        Whether to include future codes. Defaults to False.

    Methods:
    --------
    get_codes()
        Gets the codes from Klass, assigns a pandas dataframe to the .data attribute. Gets called during initialization, so usually unnecessary to run manually.
    change_dates()
        Change the dates of the codes. Runs get_codes() again after changing the dates.
    to_dict()
        Extracts two columns from the data, turning them into a dict.
        If you specify a value for "other", returns a defaultdict instead
    pivot_level()
        Pivots the data, adding the levels as suffixes to the column-names,
        Joining children codes onto their parentCodes.
        For example instead of "code", gives you "code_1", "code_2" etc.

    Attributes:
    ----------
    data : pd.DataFrame
        The pandas dataframe of the codes.

    classification_id : str
        The classification id.
    from_date : str
        The start date of the time period. "YYYY-MM-DD"
    to_date : str
        The end date of the time period. "YYYY-MM-DD"

    Raises:
    ------
    ValueError
        if from_date or to_date is not a valid date or date-string YYYY-MM-DD.
        if select_codes contains anything except numbers and the special characters *-,
        if select_level is anything except a whole number,
        if presentation_name_pattern is not a valid pattern.
        if language is not "nb", "nn" or "en".
        if include_future is not a bool.
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
        """Gets the data from the KLASS-api belonging to the code-list."""
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
        """Returns a copy-pasteable string to recreate the object."""
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
        """Prints a readable string of the codelist, including some of its attributes."""
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
    ) -> None:
        """Change the dates of the codelist, and gets the data again based on new dates.

        Parameters
        ----------
        from_date : str
            The start date of the time period.
        to_date : str
            The end date of the time period.
        include_future : bool
            Whether to include future codes.

        Returns:
        -------
        None
            Changes the dates on the class, and swaps out the data on the .data-attribute.

        Raises:
        ------
        ValueError
            if from_date or to_date is not a valid date or date-string YYYY-MM-DD.
        """
        if not from_date:
            from_date = datetime.now().strftime("%Y-%m-%d")
        if include_future is not None:
            self.include_future = include_future
        self.from_date = from_date
        self.to_date = to_date
        self.get_codes()

    def get_codes(self) -> None:
        """Retrieve codes from the classification specified by self.classification_id at a specific time.

        If self.to_date is not None, codes will be retrieved from the date range specified
        by self.from_date and self.to_date. Otherwise, codes will be retrieved only for
        the date specified by self.from_date.

        Returns:
        -------
        None
            Changes the data on the .data-attribute.
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

    def to_dict(
        self,
        key: str = "code",
        value: str = "",  # default is "name" if not set
        other: str = "",
    ) -> dict[str, str] | defaultdict[str, str]:
        """Extracts two columns from the data, turning them into a dict.

        If you specify a value for "other", returns a defaultdict instead

        Parameters
        ----------
        key : str
            The name of the column with the values you want as keys.
        value : str
            The name of the column with the values you want as values in your dict.
        other : str
            If key is missing from dict, return this value instead, if you specify a OTHER-value.

        Returns:
        -------
        dict | defaultdict
            The extracted columns as a dict or defaultdict.

        Raises:
        ------
        ValueError
            If the value is not specified and the pattern is not specified.

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
        """Pivots levels into seperate columns, and numbers columns based on levels as suffixes.

        Joining children codes onto their parentCodes.
        For example instead of "code", gives you "code_1", "code_2" etc.

        First envisioned by @mfmssb

        Parameters
        ---
        keep: list[str]
            The start of the names of the columns you want to keep when done.
            Default is ["code", "name"], but other possibilites are "presentationName",
            "level", "shortName", "validTo", "validFrom" and "notes"

        Returns:
        ---
        pd.DataFrame

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
