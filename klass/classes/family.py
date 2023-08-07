from ..requests.klass_requests import classificationfamilies_by_id
from .classification import KlassClassification


class KlassFamily:
    """
    A class to represent a classification family.
    This class is used to represent a classification family.
    It is used to get information about a classification family.
    
    """
    def __init__(self, family_id: str):
        for key, value in classificationfamilies_by_id(family_id).items():
            setattr(self, key, value)
        new_classifications = []
        for cl in self.classifications:
            new_classifications.append(
                {"classification_id": cl["_links"]["self"]["href"].split("/")[-1], **cl}
            )
        self.classifications = new_classifications

    @staticmethod
    def get_classification(classification_id: str) -> KlassClassification:
        return KlassClassification(classification_id)

    def list_classifications(self) -> list:
        return [KlassClassification(cl["classification_id"]) for cl in self.classifications]