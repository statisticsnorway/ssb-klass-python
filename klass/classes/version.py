from ..requests.klass_requests import version_by_id


class KlassVersion():
    def __init__(self, version_id: str):
        for key, value in version_by_id(version_id).items():
            setattr(self, key, value)