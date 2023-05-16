from ..requests.klass_requests import classification_search, classificationfamilies
from .classification import KlassClassification


class KlassSearchClassifications:
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

        # If you enter a number, replace with name of the classification
        if query.isdigit() and query != "":
            result = KlassClassification(query)
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
        print(self.classifications)
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
            if no_dupes:
                classification_replace = []
                seen = []
                for cl in self.classifications:
                    if cl["classification_id"] not in seen:
                        classification_replace.append(cl)
                        seen.append(cl["classification_id"])
                self.classifications = classification_replace

    @staticmethod
    def get_classification(classification_id: str) -> KlassClassification:
        return KlassClassification(classification_id)

    def __str__(self):
        return str(self.__dict__)

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
        result = classificationfamilies(
            ssbsection=ssbsection,
            include_codelists=include_codelists,
            language=language,
        )
        self.families = result["_embedded"]["classificationFamilies"]
        self.links = result["_links"]
        families_replace = []
        for fam in self.families:
            fam["family_id"] = int(fam["_links"]["self"]["href"].split("/")[-1])
            families_replace.append(fam)
        self.families = families_replace

    def __str__(self):
        result = ""
        for fam in self.families:
            result += f"{fam['family_id']} - {fam['name']} - Number of classifications: {fam['numberOfClassifications']}\n"
        return result

    def simple_search_result(self):
        result = ""
        for fl in self.families:
            result += f'ID {fl["family_id"]} - {fl["name"]}: Contains {fl["numberOfClassifications"]} Classifications\n'
        return result
