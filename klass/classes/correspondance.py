from calendar import monthrange
from datetime import date

import dateutil.parser
import pandas as pd

from ..requests.klass_requests import correspondance_table_by_id, corresponds


class KlassCorrespondance:
    def __init__(
        self,
        correspondance_id: str = "",
        source_classification_id: str = "",
        target_classification_id: str = "",
        from_date: str = "",
        to_date: str = "",
        contain_quarter: int = 0,
        language: str = "nb",
        include_future: bool = False,
    ):
        self.correspondance_id = correspondance_id
        self.source_classification_id = source_classification_id
        self.target_classification_id = target_classification_id
        self.from_date = from_date
        self.to_date = to_date
        self.contain_quarter = contain_quarter
        self.language = language
        self.include_future = include_future
        self.get_correspondance()

    def last_date_of_quarter(self) -> str:
        if isinstance(self.from_date, str):
            year = dateutil.parser.parse(self.from_date).year
        else:
            year = self.from_date.year
        last_month_of_quarter = 3 * self.contain_quarter
        date_of_last_day_of_quarter = date(
            year, last_month_of_quarter, monthrange(year, last_month_of_quarter)[1]
        )
        return str(date_of_last_day_of_quarter)

    def get_correspondance(self):
        if self.correspondance_id:
            result = correspondance_table_by_id(
                self.correspondance_id, language=self.language
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
                self.to_date = self.last_date_of_quarter()
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
                "Please set correspondance ID, or source and target classification IDs + from_date"
            )
        self.data = pd.json_normalize(self.correspondence)

    def __str__(self):
        return f"""Klass Correspondance
        id: {self.correspondance_id}
        source id: {self.source_classification_id}
        target id: {self.target_classification_id}
        from date: {self.from_date}
        to date: {self.to_date}

        Data preview (get the dataframe from the .data attribute):
        {self.data[self.data.columns[:5]].head(5)}
        """

    def __repr__(self):
        result = "KlassCorrespondance("
        if self.correspondance_id:
            result += f"correspondance_id={self.correspondance_id}, "
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
