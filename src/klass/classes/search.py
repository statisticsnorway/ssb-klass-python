from typing_extensions import Self

from klass.classes.classification import KlassClassification
from klass.classes.family import KlassFamily
from klass.requests.klass_requests import classification_search
from klass.requests.klass_requests import classificationfamilies
from klass.requests.types import ClassificationFamiliesPartWithNumberType
from klass.requests.types import ClassificationSearchResultsPartType


class KlassSearchClassifications:
    """Use to search for classifications.

    Attributes:
        classifications (list): A list of KlassClassification objects.
        query (str): The search query.
        include_codelists (bool): Whether to include codelists in the search results.
        ssbsection (str): The SSB section who owns the classification you are searching for.
        no_dupes (bool): Whether to remove duplicates from the search results.

    Args:
        query (str): The search query.
        include_codelists (bool): Whether to include codelists in the search results.
        ssbsection (str): The SSB section who owns the classification you are searching for.
        no_dupes (bool): Whether to remove duplicates from the search results.
            (Usually caused by languages showing up multiple times)
    """

    def __init__(
        self,
        query: str = "",
        include_codelists: bool = True,  # Opposite default of API, cause why not
        ssbsection: str = "",
        no_dupes: bool = False,
    ):
        """Get data from the KLASS-api, setting it as attributes on this object."""
        self.query = query
        self.include_codelists = include_codelists
        self.ssbsection = ssbsection
        self.no_dupes = no_dupes
        self.get_search()

    def get_search(self) -> None:
        """Call during init, actually get the data from the KLASS-API."""
        # If you enter a number, replace with name of the classification
        if self.query.isdigit() and self.query != "":
            actual_classification = KlassClassification(self.query)
            print(actual_classification.name)
            self.query = "".join(
                [c for c in actual_classification.name if c.isalnum() or c == " "]
            )
        elif not self.query and self.ssbsection:
            self.query = " "

        result = classification_search(
            query=self.query,
            include_codelists=self.include_codelists,
            ssbsection=self.ssbsection,
        )

        self.links = result["_links"]
        if "_embedded" in result:
            self.classifications = self._clean_classifications(
                result["_embedded"]["searchResults"], self.no_dupes
            )
        else:
            self.classifications = []

    @staticmethod
    def _clean_classifications(
        classifications: list[ClassificationSearchResultsPartType],
        no_dupes: bool = False,
    ) -> list[ClassificationSearchResultsPartType]:
        """Extract id from each classification, removing dupes.

        Args:
            classifications (list): The classifications to clean.
            no_dupes (bool): Set to True if you want equal results to be filtered out.

        Returns:
            list: The cleaned classifications.
        """
        classification_replace: list[ClassificationSearchResultsPartType] = []
        seen = []
        # Allows for the search to be an empty list, if we got something weird back
        if len(classifications) and isinstance(classifications, list):
            for cl in classifications:
                cl = {
                    "classification_id": int(
                        cl["_links"]["self"]["href"].split("/")[-1]
                    ),
                    **cl,
                }
                if cl["classification_id"] not in seen and no_dupes:
                    classification_replace.append(cl)
                    seen.append(cl["classification_id"])
                else:
                    classification_replace.append(cl)
        return classification_replace

    def __str__(self) -> str:
        """Print a readable representation of the SearchClassification-object. List the found classifications."""
        classifications_string = "\n\t".join(
            [
                ": ".join([str(c["classification_id"]), c["name"]])
                for c in self.classifications
            ]
        )
        return f"""The search for "{self.query}" returned the following classifications:
        {classifications_string}"""

    def __repr__(self) -> str:
        """Print a string representation of how to recreate the current SearchClassification-object."""
        result = f'KlassSearchClassifications(query="{self.query}", '
        if not self.include_codelists:
            result += f'include_codelists="{self.include_codelists}", '
        if self.ssbsection:
            result += f'ssbsection="{self.ssbsection}", '
        if self.no_dupes:
            result += f"no_dupes={self.no_dupes}"
        result += ")"
        return result

    @staticmethod
    def get_classification(
        classification_id: str, language: str = "nb", include_future: bool = False
    ) -> KlassClassification:
        """Get a Classification from the search object.

        Args:
            classification_id (str): The classification ID to get.
            language (str): The language to get the classification in.
                Default: "nb" for Norwegian, "nn" for Nynorsk, "en" for English.
            include_future (bool): Whether to include future codelists.

        Returns:
            KlassClassification: The classification object.
        """
        return KlassClassification(classification_id, language, include_future)

    def simple_search_result(self) -> str:
        """Reformat the resulting search into a simple string.

        Returns:
            str: The resulting reformatted string from the search results.
        """
        result = ""
        if len(self.classifications):
            for cl in self.classifications:
                result += f'{cl["classification_id"]}: {cl["name"]}\n'
        else:
            result = "Found no classifications"
        return result


class KlassSearchFamilies:
    """Search for families in the Klass API.

    Args:
        ssbsection (str): The SSB section who owns the family you are searching for.
        include_codelists (bool): Whether to include codelists in the search.
        language (str): The language to use in the search.
    Default: "nb" for Norwegian, "nn" for Nynorsk, "en" for English.
    """

    def __init__(
        self,
        ssbsection: str = "",
        include_codelists: bool = False,
        language: str = "nb",
    ):
        """Get data from the KLASS-api, setting it as attributes on this object."""
        self.ssbsection = ssbsection
        self.include_codelists = include_codelists
        self.language = language
        self.get_search()

    def __str__(self) -> str:
        """Print a human readable string of the families found, and how many classifications they contain."""
        result = ""
        for fam in self.families:
            result += f"Family ID: {fam['family_id']} - {fam['name']} - "
            result += f"Number of classifications: {fam['numberOfClassifications']}\n"
        return result

    def __repr__(self) -> str:
        """Get a representation of how to recreate this SearchFamilies-object."""
        result = "KlassSearchFamilies("
        if self.ssbsection:
            result += f'ssbsection="{self.ssbsection}", '
        if self.include_codelists:
            result += f"include_codelists={self.include_codelists}, "
        if self.language != "nb":
            result += f'language="{self.language}"'
        result += ")"
        return result

    def get_search(self) -> Self:
        """Get the search result from the API and reformat it into the .families and .links attributes.

        This should be run after any change to the .ssbsection, .include_codelists, or .language
        attributes.

        Returns:
            self (KlassSearchFamilies): Returns self to make the method more easily chainable.
        """
        result = classificationfamilies(
            ssbsection=self.ssbsection,
            include_codelists=self.include_codelists,
            language=self.language,
        )
        if "_embedded" in result:
            self.families: list[ClassificationFamiliesPartWithNumberType] = result[
                "_embedded"
            ]["classificationFamilies"]
        else:
            self.families = []
        self.links = result["_links"]
        families_replace = []
        # Allows for the search to be an empty list, if we got something weird back
        if isinstance(self.families, list) and len(self.families):
            for fam in self.families:
                fam["family_id"] = fam["_links"]["self"]["href"].split("/")[-1]
                families_replace.append(fam)
        self.families = families_replace
        return self

    def get_family(self, family_id: str = "0") -> KlassFamily:
        """Return a KlassFamily object of the family with the given ID.

        If no ID is given, chooses the first Family returned by the search.

        Args:
            family_id (str): The family ID to get.

        Returns:
            KlassFamily: The family object.
        """
        if not family_id:
            family_id = self.families[0]["family_id"]
        return KlassFamily(str(family_id))

    def simple_search_result(self) -> str:
        """Reformat the resulting search into a simple string.

        Returns:
            str: The resulting reformatted string from the search results.
        """
        result = ""
        for fl in self.families:
            result += f'ID {fl["family_id"]} - {fl["name"]}: '
            result += f'Contains {fl["numberOfClassifications"]} Classifications\n'
        return result
