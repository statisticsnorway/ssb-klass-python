from ..classes.classification import KlassClassification


def get_classification(classification_id: str) -> KlassClassification:
    """Simple factory-function to create instances of KlassClassifications (classes are scary)."""
    return KlassClassification(classification_id)
