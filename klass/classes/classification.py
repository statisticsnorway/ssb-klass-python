from ..requests.klass_requests import classification_by_id
from .correspondance import KlassCorrespondance
from .version import KlassVersion
from .codes import KlassCodes


class KlassClassification:

    def __init__(self,
                 classification_id: str,
                 language: str = "nb",
                 include_future: bool = False):
        self.classification_id = classification_id
        self.language = language
        self.include_future = include_future

        for key, value in classification_by_id(classification_id,
                                               language=language,
                                               include_future=include_future).items():
            setattr(self, key, value)

        version_replace = []
        for ver in self.versions:
            version_replace.append(
                {"version_id": int(ver["_links"]["self"]["href"].split("/")[-1]),
                 **ver}
            )
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

    def __repr__(self):
        result = f"KlassClassification(classification_id='{self.classification_id}', "
        if self.selected_language != "nb":
            result += f"language='{self.selected_language}', "
        if self.selected_future:
            result += "include_future=True, "
        result += ")"
        return result

    @staticmethod
    def get_version(version_id) -> KlassVersion:
        return KlassVersion(version_id)

    def get_correspondance_to(target_classification_id: str,
                              from_date: str,
                              to_date: str = "",
                              language: str = "",
                              include_future: bool = None,
                             ) -> KlassCorrespondance:
        if language == "":
            language = self.selected_language
        if include_future is None:
            include_future = self.selected_future
        return KlassCorrespondance(source_classification_id=self.classification_id,
                                   target_classification_id=target_classification_id,
                                   from_date=from_date,
                                   to_date=to_date,
                                   language=language,
                                   include_future=include_future,
                                  )

    def get_codes(self,
                  from_date: str = "",
                  to_date: str = "",
                  language: str = "",
                  include_future: bool = None) -> KlassCodes:
        # If not passed to method, grab these from the Classification
        if language == "":
            language = self.language
        if include_future is None:
            include_future = self.include_future

        return KlassCodes(classification_id = self.classification_id,
                          from_date= from_date,
                          to_date=to_date,
                          language=language,
                          include_future=include_future)