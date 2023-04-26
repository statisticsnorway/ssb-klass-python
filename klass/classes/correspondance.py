from ..requests.klass_requests import corresponds, corresponds_at, correspondance_table_by_id


class KlassCorrespondance():
    def __init__(self,
                 correspondance_id: str = "",
                 source_classification_id: str = "",
                 target_classification_id: str = "",
                 from_date: str = "",
                 to_date: str = "",
                 language: str = "nb",
                 include_future: bool = False):
        self.correspondance_id = correspondance_id
        self.source_classification_id = source_classification_id
        self.target_classification_id = target_classification_id
        self.from_date = from_date
        self.to_date = to_date
        self.language = language
        self.include_future = include_future
        
        if correspondance_id:
            json_content = correspondance_table_by_id(correspondance_id, language=language)
        elif source_classification_id and target_classification_id and from_date:
            json_content = corresponds(source_classification_id=source_classification_id,
                               target_classification_id=target_classification_id,
                               from_date=from_date,
                               to_date=to_date,
                               language=language,
                               include_future=include_future
                               )
        else:
            raise ValueError("Please set correspondance ID, or source and target classification IDs")
        for key, value in json_content.items():
            setattr(self, key, value)
            
            
    def __str__(self):
        return self.__dict__
    
    
    def __repr__(self):
        result = "KlassCorrespondance("
        if self.correspondance_id:
            result += f"correspondance_id={self.correspondance_id}, "
        if self.source_classification_id:
            result += f"source_classification_id={self.source_classification_id}, "
        if self.target_classification_id:
            result += f"target_classification_id={self.target_classification_id}, "
        if self.from_date:
            result += f"from_date={self.from_date}, "
        if self.to_date:
            result += f"to_date={self.to_date}, "
        if self.language != "nb":
            result += f"language={self.language}, "
        result += ")"
        return result
        
    