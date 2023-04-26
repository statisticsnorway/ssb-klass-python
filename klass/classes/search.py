from ..requests.klass_requests import classification_search, classificationfamilies
from .classification import KlassClassification


class KlassSearchClassifications():
    def __init__(self,
                 query: str = "",
                 include_codelists: bool = False,
                 ssbsection: str = ""):
        self.query = query
        self.include_codelists = include_codelists
        self.ssbsection = ssbsection
        result = classification_search(query=self.query,
                                    include_codelists=self.include_codelists,
                                    ssbsection=self.ssbsection)
        self.classifications = result["_embedded"]["searchResults"]
        self.links = result["_links"]
        classification_replace = []
        for cl in self.classifications:
            cl = {"classification_id": int(
                    cl["_links"]["self"]["href"].split("/")[-1]
                  ), **cl}
            classification_replace.append(cl)
        self.classifications = classification_replace

    @staticmethod
    def get_classification(classification_id: str) -> KlassClassification:
        return KlassClassification(classification_id)


class KlassSearchFamilies():
    def __init__(self,
                 ssbsection: str = "",
                 include_codelists: bool = False,
                 language: str = "nb",):
        result = classificationfamilies(ssbsection=ssbsection,
                                             include_codelists=include_codelists,
                                             language=language,)
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
