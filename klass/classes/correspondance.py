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
        for key, value in json_content.items():
            setattr(self, key, value)
            
            
    def __str__(self):
        return self.__dict__
    
    
    def __repr__(self):
        
        if self.correspondance_id:
            pass
        if self.source_classification_id:
            pass
        if self.target_classification_id:
            pass
        if self.from_date:
            pass
        
    