from ..classes.classification import KlassClassification


def get_classification(classification_id: str) -> KlassClassification:
    return KlassClassification(classification_id)
