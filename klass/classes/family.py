from ..requests.klass_requests import classificationfamilies_by_id
from .classification import KlassClassification


class KlassFamily:
    """
    A class to represent a classification family.
    This class is used to represent a classification family.
    It is used to get information about a classification family.
    
    """
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

    def get_classification(self, classification_id: str = "") -> KlassClassification:
        if not classification_id:
            classification_id = self.classifications[0]["classification_id"]
        return KlassClassification(classification_id)

    def __str__(self):
        classifications_string = "\n\t".join(
            [
                ": ".join([c["classification_id"], c["name"]])
                for c in self.classifications
            ]
        )
        return f"""The Klass Family "{self.name}" has id {self.family_id}.
And contains the following classifications:
\t{classifications_string}
        """

    def __repr__(self):
        return f"KlassFamily({self.family_id})"
