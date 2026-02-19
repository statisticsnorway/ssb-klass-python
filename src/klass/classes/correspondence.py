from calendar import monthrange
from collections import defaultdict
from datetime import date

import dateutil.parser
import pandas as pd
from typing_extensions import Self
from typing_extensions import overload

from ..requests.klass_requests import correspondence_table_by_id
from ..requests.klass_requests import corresponds
from ..requests.klass_types import CorrespondsType
from ..requests.klass_types import Language
from ..requests.klass_types import T_correspondanceMaps
from ..utility.filters import limit_na_level


class KlassCorrespondence:
    """Correspondences in Klass exist between two classifications at a specific time (hence actually between Versions).

    They are used to translate data between two classifications.
    For example, from geographical municipality up to county level.

    You can identify the correspondence by their individual ids,
    or by the source classification ID + the target classification ID + a specific time.

    Args:
        correspondence_id: The ID of the correspondence.
        source_classification_id: The ID of the source classification.
        target_classification_id: The ID of the target classification.
        from_date: The start date of the correspondence.
        to_date: The end date of the correspondence.
        contain_quarter: The number of quarters the correspondence should contain,
            this replaces the to_date during initialization.
        language: The language of the correspondence. "nb", "nn" or "en".
        include_future: If the correspondence should include future correspondences.
    """

    @overload
    def __init__(
        self: Self,
        correspondence_id: str | int = ...,
        source_classification_id: None = ...,
        target_classification_id: None = ...,
        from_date: None = ...,
        to_date: None = ...,
        contain_quarter: int = ...,
        language: Language = ...,
        include_future: bool = ...,
    ) -> None: ...

    @overload
    def __init__(
        self: Self,
        correspondence_id: None = ...,
        source_classification_id: str | int = ...,
        target_classification_id: str | int = ...,
        from_date: str = ...,
        to_date: str | None = ...,
        contain_quarter: int = ...,
        language: Language = ...,
        include_future: bool = ...,
    ) -> None: ...

    def __init__(
        self: Self,
        correspondence_id: str | int | None = None,
        source_classification_id: str | int | None = None,
        target_classification_id: str | int | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        contain_quarter: int = 0,
        language: Language = "nb",
        include_future: bool = False,
    ) -> None:
        self.correspondence_id = correspondence_id
        self.source_classification_id = source_classification_id
        self.target_classification_id = target_classification_id
        self.from_date = from_date
        self.to_date = to_date
        self.contain_quarter = contain_quarter
        self.language: Language = language
        self.include_future = include_future

        self.get_correspondence()

    def __str__(self) -> str:
        """Print the correspondence in a human readable format, including some attributes/metadata."""
        return f"""Klass Correspondence
        id: {self.correspondence_id}
        source id: {self.source_classification_id}
        target id: {self.target_classification_id}
        from date: {self.from_date}
        to date: {self.to_date}

        Data preview (get the dataframe from the .data attribute):
        {self.data[self.data.columns[:5]].head(5)}
        """

    def __repr__(self) -> str:
        """Return a string representation of the correspondence-object, including the parameters used to recreate it."""
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

    def get_correspondence(self) -> Self:
        """Run as the last part of initialization. Actually setting the data from the API as attributes.

        If you reset some attributes, maybe run this after to "update" the data of the correspondence.

        Gets and reshapes correspondences based on attributes on the class.

        Returns:
            Self: Returns self to make the method more easily chainable.

        Raises:
            ValueError: If you are filling out the wrong combination of correspondence_id, source_classification_id,
                target_classification_id and from_date, we cant get make a correct query to the API.
        """
        if self.correspondence_id:
            result_id = correspondence_table_by_id(
                self.correspondence_id, language=self.language
            )
            self.name: str = result_id["name"]
            self.contactPerson: dict[str, str] = result_id["contactPerson"]
            self.owningSection: str = result_id["owningSection"]
            self.source: str = result_id["source"]
            self.sourceId: int = result_id["sourceId"]
            self.target: str = result_id["target"]
            self.targetId: int = result_id["targetId"]
            self.changeTable: bool = result_id["changeTable"]
            self.lastModified: str = result_id["lastModified"]
            self.published: list[str] = result_id["published"]
            self.sourceLevel: str | None = result_id["sourceLevel"]
            self.targetLevel: str | None = result_id["targetLevel"]
            self.description: str = result_id["description"]
            self.changelogs: list[str] = result_id["changelogs"]
            self.correspondenceMaps: T_correspondanceMaps = result_id[
                "correspondenceMaps"
            ]
            self.correspondence: T_correspondanceMaps = self.correspondenceMaps
            del self.correspondenceMaps
        elif (
            self.source_classification_id
            and self.target_classification_id
            and self.from_date
        ):
            if self.contain_quarter:
                self.to_date = self._last_date_of_quarter()
            result: CorrespondsType = corresponds(
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
        return self

    def _last_date_of_quarter(self) -> str:
        """Calculate the last date of the quarter.

        Uses the attribute "contain_quarter" to determine which quarter to use.

        Returns:
            str: The last date of the quarter.

        Raises:
            ValueError: if from date is missing
        """
        if not self.from_date:
            raise ValueError(
                "Can't calculate the last date of the quarter without from_date"
            )
        from_date = dateutil.parser.parse(self.from_date)
        year = from_date.year
        last_month_of_quarter = 3 * self.contain_quarter
        date_of_last_day_of_quarter = date(
            year, last_month_of_quarter, monthrange(year, last_month_of_quarter)[1]
        )
        return str(date_of_last_day_of_quarter)

    def to_dict(
        self,
        key: str = "sourceCode",
        value: str = "targetCode",
        other: str | None = None,
        remove_na: bool = True,
        select_level: int | None = None,
    ) -> dict[str, str | None] | defaultdict[str, str | None]:
        """Extract two columns from the data, turning them into a dict.

        If you specify a value for "other", returns a defaultdict instead.

        Columns in the data are 'sourceCode', 'sourceName', 'sourceShortName',
        'targetCode', 'targetName', 'targetShortName', 'validFrom', 'validTo'.

        Args:
            key: The name of the column with the values you want as keys.
            value: The name of the column with the values you want as values in your dict.
            other: The value to use for keys that don't exist in the data.
            remove_na: Set to False if you want to keep empty mappings over the key and value columns. Empty is defined as empty strings or NA-types.
            select_level: Keep only a specific level defines the variants codes / groups.

        Returns:
            dict[str, str | None] | defaultdict[str, str | None]: The dictionary of the correspondence.
        """
        data = self.data.copy()
        value_col = value
        if value == "presentationName" and "name" in data.columns:
            value_col = "_value_fallback"
            data[value_col] = data["presentationName"].astype("string[pyarrow]").fillna("")
            empty_mask = data[value_col] == ""
            if empty_mask.any():
                data.loc[empty_mask, value_col] = data["name"].astype("string[pyarrow]")
        limit_data = limit_na_level(data, key, value_col, remove_na, select_level)
        mapping = dict(zip(limit_data[key], limit_data[value_col], strict=False))
        if other:
            mapping = defaultdict(lambda: other, mapping)
        return mapping
