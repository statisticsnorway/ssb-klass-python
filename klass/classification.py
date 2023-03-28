import klass_requests as klass


class KlassClassification:
    def __init__(self, classification_id: str):
        for key, value in klass.classification_by_id(classification_id).items():
            setattr(self, key, value)
