from ..requests.klass_requests import classificationfamilies_by_id
from .classification import KlassClassification


class KlassClassificationFamily():
    def __init__(self, family_id: str):
        for key, value in classificationfamilies_by_id(family_id).items():
            setattr(self, key, value)
        new_classifications = []
        for cl in self.classifications:
            new_classifications.append({"classification_id": cl['_links']['self']['href'].split("/")[-1], **cl})
        self.classifications = new_classifications
    
    @staticmethod
    def get_classification(classification_id: str) -> KlassClassification:
        return KlassClassification(classification_id)