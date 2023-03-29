import pandas as pd
from ..requests.klass_requests import version_by_id


class KlassVersion:
    def __init__(self, version_id: str):
        self.version_id = version_id
        for key, value in version_by_id(version_id).items():
            setattr(self, key, value)
            
    def __str__(self):
        contact = "Contact Person:\n"
        for k, v in self.contactPerson.items():
            contact += f"\t{k}: {v}\n"

        result = f"""Version {self.version_id}: {self.name}
        Owning Section: {self.owningSection}
        Valid: {self.validFrom} -> {self.validTo}
        Last modified: {self.lastModified}
        {contact}
        
        Number of correspondances: {len(self.correspondenceTables)}
        Number of classification variants: {len(self.classificationVariants)}
        Number of classification items: {len(self.classificationItems)}
        Number of levels: {len(self.levels)}
        
        
{self.introduction}
        """
        return result
    
    def classification_items(self, select_level: int = 0):
        data = pd.json_normalize(self.classificationItems)
        if not str(select_level).isdigit():
            select_level = {item["levelName"]: item["levelNumber"] for item in self.levels}[select_level]
        if select_level:
            data = data[data["level"].astype(str) == str(select_level)]
        return data