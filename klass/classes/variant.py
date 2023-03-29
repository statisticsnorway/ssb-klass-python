from ..requests.klass_requests import variant, variant_at


class KlassVariant():
    def __init__(self, 
                 variant_id: str = "",
                 classification_id: str = "",
                 variant_name: str = "",
                 from_date: str = "",
                 to_date: str = "",
                 presentation_name_pattern: str = "",
                 language: str = "nb",
                 include_future: bool = False,
                ):
        if variant_id:
            json = variant_by_id(variant_id, language=language)
        elif to_date:
            json = variant()
        