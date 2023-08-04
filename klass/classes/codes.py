from collections import defaultdict
from datetime import datetime

import pandas as pd

from ..requests.klass_requests import codes, codes_at


class KlassCodes:
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

    def __repr__(self):
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

    def __str__(self):
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

    def get_codes(self):
        """
        Retrieve codes from the classification specified by self.classification_id.

        If self.to_date is not None, codes will be retrieved from the date range specified
        by self.from_date and self.to_date. Otherwise, codes will be retrieved only for
        the date specified by self.from_date.

        Parameters
        ----------
        self : object
            Instance of a class containing classification_id, from_date, to_date,
            select_codes, select_level, presentation_name_pattern, language,
            and include_future attributes.

        Returns
        -------
        data : object
            Object containing retrieved codes, with properties dependent on the API
            used to retrieve them.

        Raises
        ------
        Any exceptions raised by the codes() or codes_at() functions called within
        this method.
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
    ) -> dict | defaultdict:
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

    def wide_data(self, keep: list[str] = None) -> pd.DataFrame:
        """Pivots levels into seperate columns, and numbers columns based on levels.

        Parameters
        ---
        keep: list[str]
            The start of the names of the columns you want to keep when done.
            Default is ["code", "name"], but other possibilites are "presentationName",
            "level", "shortName", "validTo", "validFrom" and "notes"

        Returns
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
