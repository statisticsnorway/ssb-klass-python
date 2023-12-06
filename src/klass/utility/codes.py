import pandas as pd

from ..classes.codes import KlassCodes


def get_codes(
    classification_id: str = "", date: str = "", dataframe: bool = False
) -> KlassCodes | pd.DataFrame:
    """Get the codelist-data from a classification as a dataframe, or a KlassCodes-wrapper (includes metadata)."""
    if dataframe:
        return KlassCodes(classification_id, date).data
    return KlassCodes(classification_id, date)
