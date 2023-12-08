from klass.classes.classification import KlassClassification
from klass.requests.klass_requests import classificationfamilies_by_id
from klass.requests.types import ClassificationFamiliesByIdType
from klass.requests.types import ClassificationPartWithType


class KlassFamily:
    """Families represent "general statistical areas" like "Education".

    Families in Klass "own" / "have" several classifications.
    Families are owned by sections (a part of Statistics Norway who is responsible for the family).

    Attributes:
        classifications (list): A list of classifications in the family.
        family_id (str): The ID of the family.
        name (str): The name of the family.
        _links (dict): A dictionary of API links referencing itself.

    Args:
        family_id (str): The ID of the family.
    """

    def __init__(self, family_id: str):
        """Get the family data from the klass-api, setting it as attributes on the object."""
        self.family_id = family_id
        # Setting for mypy
        result: ClassificationFamiliesByIdType = classificationfamilies_by_id(
            self.family_id
        )
        self.name: str = result["name"]
        classifications_temp: list[ClassificationPartWithType] = result[
            "classifications"
        ]
        self._links: dict[str, dict[str, str]] = result["_links"]

        new_classifications: list[ClassificationPartWithType] = []
        for cl in classifications_temp:
            new_classifications.append(
                {"classification_id": cl["_links"]["self"]["href"].split("/")[-1], **cl}
            )
        self.classifications: list[ClassificationPartWithType] = new_classifications

    def __str__(self) -> str:
        """Print representation of the KLASS-family. Contains all the ids for its classifications."""
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

    def __repr__(self) -> str:
        """Representation of the object, and how to recreate it."""
        return f"KlassFamily({self.family_id})"

    def get_classification(self, classification_id: str = "") -> KlassClassification:
        """Get a classification from the family.

        Args:
            classification_id (str): The ID of the classification.
                If not given, the first classification in the family is returned based on its ID.

        Returns:
            KlassClassification: The classification.
        """
        if not classification_id:
            classification_id = self.classifications[0]["classification_id"]
        return KlassClassification(classification_id)
