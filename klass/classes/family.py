from ..requests.klass_requests import classificationfamilies_by_id

class KlassClassificationFamily():
    def __init__(self, family_id: str):
        for key, value in classificationfamilies_by_id(family_id).items():
            setattr(self, key, value)