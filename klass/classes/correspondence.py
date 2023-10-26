from calendar import monthrange
from collections import defaultdict
from datetime import date
from typing import Union

import dateutil.parser
import pandas as pd

from ..requests.klass_requests import correspondence_table_by_id, corresponds


class KlassCorrespondence:
    """Correspondences in Klass exist between two classifications at a specific time,
    (hence actually between Versions).
    They are used to translate data between two classifications.
    For example from geographical municipality up to county level.

    You can identify the correspondence by their individual ids,
    or by the source classification ID + the target classification ID + a specific time.

    Parameters
    ----------
    correspondence_id : str
        The id of the correspondence.
    source_classification_id : str
        The id of the source classification.
    target_classification_id : str
        The id of the target classification.
    from_date : str
        The start date of the correspondence.
    to_date : str (optional)
        The end date of the correspondence.
    contain_quarter : int
        The number of quarters the correspondence should contain,
        this replaces the to_date during initialization.
    language : str
        The language of the correspondence. "nb", "nn" or "en".
    include_future : bool
        If the correspondence should include future correspondences.

    Methods
    -------
    to_dict()
        Extracts two columns from the data, turning them into a dict.
        If you specify a value for "other", returns a defaultdict instead.
        Columns in the data are 'sourceCode', 'sourceName', 'sourceShortName'
        'targetCode', 'targetName', 'targetShortName', 'validFrom', 'validTo'
    get_correspondence()
        Run as last part of initialization.
        If you reset some attributes, maybe run this after to "update" the data of the correspondence.
    _last_date_of_quarter()
        Returns the last date of the numbered quarter provided.

    Attributes
    ----------
    data : pd.DataFrame
        The pandas dataframe of the correspondences.
    correspondence : list
        The list of the correspondences returned by the API.
    correspondence_id : str
        The id of the correspondence.
    source_classification_id : str
        The id of the source classification.
    target_classification_id : str
        The id of the target classification.
    from_date : str
        The start date of the correspondence.
    to_date : str (optional)
        The end date of the correspondence.
    contain_quarter : int
        The number of quarters the correspondence should contain,
        this replaces the to_date during initialization.
    language : str
        The language of the correspondence. "nb", "nn" or "en".
    include_future : bool
        If the correspondence should include future correspondences.
    """

    def __init__(
        self,
        correspondence_id: str = "",
        source_classification_id: str = "",
        target_classification_id: str = "",
        from_date: str = "",
        to_date: str = "",
        contain_quarter: int = 0,
        language: str = "nb",
        include_future: bool = False,
    ):
        self.correspondence_id = correspondence_id
        self.source_classification_id = source_classification_id
        self.target_classification_id = target_classification_id
        self.from_date = from_date
        self.to_date = to_date
        self.contain_quarter = contain_quarter
        self.language = language
        self.include_future = include_future
        self.get_correspondence()

    def __str__(self):
        return f"""Klass Correspondence
        id: {self.correspondence_id}
        source id: {self.source_classification_id}
        target id: {self.target_classification_id}
        from date: {self.from_date}
        to date: {self.to_date}

        Data preview (get the dataframe from the .data attribute):
        {self.data[self.data.columns[:5]].head(5)}
        """

    def __repr__(self):
        result = "KlassCorrespondence("
        if self.correspondence_id:
            result += f"correspondence_id={self.correspondence_id}, "
        if self.source_classification_id:
            result += f"source_classification_id={self.source_classification_id}, "
        if self.target_classification_id:
            result += f"target_classification_id={self.target_classification_id}, "
        if self.from_date:
            result += f"from_date={self.from_date}, "
        if self.to_date:
            result += f"to_date={self.to_date}, "
        if self.language != "nb":
            result += f"language={self.language}, "
        result += ")"
        return result

    def get_correspondence(self) -> None:
        """Run as last part of initialization.
        If you reset some attributes, maybe run this after to "update" the data of the correspondence.

        Gets and reshapes correspondences based on attributes on the class.

        Returns
        -------
        None
            Sets .data attribute based on the attributes of the class
        """
        if self.correspondence_id:
            result = correspondence_table_by_id(
                self.correspondence_id, language=self.language
            )
            for key, value in result.items():
                setattr(self, key, value)
            self.correspondence = result["correspondenceMaps"]
            del self.correspondenceMaps
        elif (
            self.source_classification_id
            and self.target_classification_id
            and self.from_date
        ):
            if self.contain_quarter:
                self.to_date = self._last_date_of_quarter()
            result = corresponds(
                source_classification_id=self.source_classification_id,
                target_classification_id=self.target_classification_id,
                from_date=self.from_date,
                to_date=self.to_date,
                language=self.language,
                include_future=self.include_future,
            )
            self.correspondence = result["correspondenceItems"]
        else:
            raise ValueError(
                "Please set correspondence ID, or source and target classification IDs + from_date"
            )
        self.data = pd.json_normalize(self.correspondence)

    def _last_date_of_quarter(self) -> str:
        """Calculates the last date of the quarter.
        Uses the attribute "contain_quarter" to determine which quarter to use.

        Returns
        -------
        str
            The last date of the quarter.
        """
        if isinstance(self.from_date, str):
            year = dateutil.parser.parse(self.from_date).year
        else:
            year = self.from_date.year
        last_month_of_quarter = 3 * self.contain_quarter
        date_of_last_day_of_quarter = date(
            year, last_month_of_quarter, monthrange(year, last_month_of_quarter)[1]
        )
        return str(date_of_last_day_of_quarter)

    def to_dict(
        self,
        key: str = "sourceCode",
        value: str = "targetCode",
        other: str = "",
    ) -> Union[dict, defaultdict]:
        """Extracts two columns from the data, turning them into a dict.
        If you specify a value for "other", returns a defaultdict instead.

        Columns in the data are 'sourceCode', 'sourceName', 'sourceShortName'
        'targetCode', 'targetName', 'targetShortName', 'validFrom', 'validTo'

        Parameters
        ----------
        key : str
            The name of the column with the values you want as keys.
        value : str
            The name of the column with the values you want as values in your dict.
        other : str
            The value to use for keys that don't exist in the data.

        Returns
        -------
        dict | defaultdict
            The dictionary of the correspondence.
        """
        mapping = dict(zip(self.data[key], self.data[value]))
        if other:
            mapping = defaultdict(lambda: other, mapping)
        return mapping
