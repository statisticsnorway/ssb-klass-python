from datetime import datetime

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

    def wide_data(self):
        return self.data.pivot_table("level")
