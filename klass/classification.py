from .klass_requests import classification_by_id


class KlassClassification:
    def __init__(self, classification_id: str):
        for key, value in classification_by_id(classification_id).items():
            setattr(self, key, value)
