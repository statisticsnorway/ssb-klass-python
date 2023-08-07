from ..requests.klass_requests import classification_search, classificationfamilies
from .classification import KlassClassification
from .family import KlassFamily


class KlassSearchClassifications:
    """Used to search for classifications.

    Parameters
    ---
    query: str
        The search query.
    include_codelists: bool
        Whether to include codelists in the search results.
    ssbsection: str
        The SSB section to search.
    """
    def __init__(
        self,
        query: str = "",
        include_codelists: bool = True,  # Opposite default of API, cause why not
        ssbsection: str = "",
        no_dupes=False,
    ):
        self.query = query
        self.include_codelists = include_codelists
        self.ssbsection = ssbsection
        self.no_dupes = no_dupes
        self.get_search()

    def get_search(self) -> None:
        # If you enter a number, replace with name of the classification
        if self.query.isdigit() and self.query != "":
            result = KlassClassification(self.query)
            print(result.name)
            self.query = "".join([c for c in result.name if c.isalnum() or c == " "])
        elif not self.query and self.ssbsection:
            self.query = " "

        result = classification_search(
            query=self.query,
            include_codelists=self.include_codelists,
            ssbsection=self.ssbsection,
        )
        if "_embedded" in result.keys():
            self.classifications = result["_embedded"]["searchResults"]
        elif "searchResults" in result.keys():
            self.classifications = result["searchResults"]
        else:
            self.classifications = []

        self.links = result["_links"]
        if len(self.classifications):
            classification_replace = []
            for cl in self.classifications:
                cl = {
                    "classification_id": int(
                        cl["_links"]["self"]["href"].split("/")[-1]
                    ),
                    **cl,
                }
                classification_replace.append(cl)
            self.classifications = classification_replace
            if self.no_dupes:
                classification_replace = []
                seen = []
                for cl in self.classifications:
                    if cl["classification_id"] not in seen:
                        classification_replace.append(cl)
                        seen.append(cl["classification_id"])
                self.classifications = classification_replace

    def __str__(self):
        classifications_string = "\n\t".join(
            [
                ": ".join([str(c["classification_id"]), c["name"]])
                for c in self.classifications
            ]
        )
        return f"""The Search returned the following classifications:
        {classifications_string}"""

    def __repr__(self):
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
    def get_classification(classification_id: str) -> KlassClassification:
        return KlassClassification(classification_id)

    def simple_search_result(self):
        result = ""
        if len(self.classifications):
            for cl in self.classifications:
                result += f'{cl["classification_id"]}: {cl["name"]}\n'
        else:
            result = "Found no classifications"
        return result


class KlassSearchFamilies:
    def __init__(
        self,
        ssbsection: str = "",
        include_codelists: bool = False,
        language: str = "nb",
    ):
        self.ssbsection = ssbsection
        self.include_codelists = include_codelists
        self.language = language
        self.get_search()

    def __str__(self):
        result = ""
        for fam in self.families:
            result += f"Family ID: {fam['family_id']} - {fam['name']} - "
            result += f"Number of classifications: {fam['numberOfClassifications']}\n"
        return result

    def __repr__(self):
        result = "KlassSearchFamilies("
        if self.ssbsection:
            result += f'ssbsection="{self.ssbsection}", '
        if self.include_codelists:
            result += f"include_codelists={self.include_codelists}, "
        if self.language != "nb":
            result += f'language="{self.language}"'
        result += ")"
        return result

    def get_search(self):
        result = classificationfamilies(
            ssbsection=self.ssbsection,
            include_codelists=self.include_codelists,
            language=self.language,
        )
        self.families = result["_embedded"]["classificationFamilies"]
        self.links = result["_links"]
        families_replace = []
        for fam in self.families:
            fam["family_id"] = int(fam["_links"]["self"]["href"].split("/")[-1])
            families_replace.append(fam)
        self.families = families_replace

    def get_family(self, family_id=0):
        if not family_id:
            family_id = self.families[0]["family_id"]
        return KlassFamily(family_id)

    def simple_search_result(self):
        result = ""
        for fl in self.families:
            result += f'ID {fl["family_id"]} - {fl["name"]}: '
            result += f'Contains {fl["numberOfClassifications"]} Classifications\n'
        return result
