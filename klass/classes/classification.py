from ..requests.klass_requests import classification_by_id
from .version import KlassVersion

class KlassClassification:


    def __init__(self, 
                 classification_id: str,
                 language: str = "nb",
                 include_future: bool = False):
        self.classification_id = classification_id
        for key, value in classification_by_id(classification_id,
                                               language=language,
                                               include_future=include_future).items():
            setattr(self, key, value)
        version_replace = []
        for ver in self.versions:
            ver["version_id"] = int(ver["_links"]["self"]["href"].split("/")[-1])
            version_replace.append(ver)
        self.versions = version_replace


    def __str__(self):
        contact = "Contact Person:\n"
        for k, v in self.contactPerson.items():
            contact += f"\t{k}: {v}\n"
        units = ", ".join(self.statisticalUnits)
        result = f"""Classification {self.classification_id}: {self.name}
        Owning Section: {self.owningSection}
        {contact}
        Statistical Units: {units}
        Number of versions: {len(self.versions)}
        
{self.description}
        """
        return result
    
    @staticmethod
    def get_version(version_id):
        return KlassVersion(version_id)