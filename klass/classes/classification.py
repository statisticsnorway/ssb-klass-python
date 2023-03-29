from ..requests.klass_requests import classification_by_id


class KlassClassification:
    def __init__(self, classification_id: str):
        for key, value in classification_by_id(classification_id).items():
            setattr(self, key, value)

    def get_version(version_name: str = "", version_id: str = ""):
        if version_name:
            return KlassVersion(version_name=version_name)