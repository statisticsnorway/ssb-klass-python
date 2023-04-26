from ..classes.codes import KlassCodes


def get_codes(classification_id, date = "", dataframe: bool = False) -> KlassCodes:
    if dataframe:
        return KlassCodes(classification_id, date).data
    return KlassCodes(classification_id, date)