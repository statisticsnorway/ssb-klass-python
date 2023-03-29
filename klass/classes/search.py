from ..requests.klass_requests import classification_search, classificationfamilies


class KlassSearchVariants():
    pass

class KlassSearchClassifications():
    pass

class KlassSearchClassificationFamilies():
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
