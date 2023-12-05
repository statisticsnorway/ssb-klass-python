from ..requests.klass_requests import T_classificationfamilies_by_id
from ..requests.klass_requests import T_classificationfamilies_by_id_classifications
from ..requests.klass_requests import classificationfamilies_by_id
from .classification import KlassClassification


class KlassFamily:
    """Families represent "general statistical areas" like "Education".

    Families in Klass "own" / "has" several classifications.
    Families are owned by sections (a part of Statistics Norway who is responsible for the family).

    Parameters
    ----------
    family_id : str
        The id of the family.

    Attributes:
    ----------
    classifications : list
        A list of classifications in the family.
    family_id : str
        The id of the family.
    name : str
        The name of the family.
    _links : dict
    A dictionary of api-links referencing itself.
    """

    def __init__(self, family_id: str):
        """Gets the family data from the klass-api, setting it as attributes on the object."""
        self.family_id = family_id
        # Setting for mypy
        result: T_classificationfamilies_by_id = classificationfamilies_by_id(
            self.family_id
        )
        self.name: str = result["name"]
        classifications_temp: list[
            T_classificationfamilies_by_id_classifications
        ] = result["classifications"]
        self._links: dict[str, dict[str, str]] = result["_links"]

        new_classifications: list[T_classificationfamilies_by_id_classifications] = []
        for cl in classifications_temp:
            new_classifications.append(
                {"classification_id": cl["_links"]["self"]["href"].split("/")[-1], **cl}
            )
        self.classifications: list[
            T_classificationfamilies_by_id_classifications
        ] = new_classifications

    def __str__(self) -> str:
        """String representation of the KLASS-family. Also containing all the ids for its classifications."""
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

        Parameters
        ----------
        classification_id : str
            The id of the classification. If not given, the first classification in the family is returned based on its ID.

        Returns:
        -------
        KlassClassification
            The classification.

        """
        if not classification_id:
            classification_id = self.classifications[0]["classification_id"]
        return KlassClassification(classification_id)
