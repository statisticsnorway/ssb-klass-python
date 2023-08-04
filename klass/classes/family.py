from ..requests.klass_requests import classificationfamilies_by_id
from .classification import KlassClassification


class KlassFamily:
    def __init__(self, family_id: str):
        self.family_id = family_id
        for key, value in classificationfamilies_by_id(self.family_id).items():
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

    def __str__(self):
        classifications_string = "\n".join(self.classifications)
        return f"""Klass Family with id {self.family_id}.
        Containing the classifications:
        {classifications_string}
        """

    def __repr__(self):
        return f"KlassFamily({self.family_id})"
