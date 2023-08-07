import pandas as pd

from ..requests.klass_requests import changes, classification_by_id
from .codes import KlassCodes
from .correspondance import KlassCorrespondance
from .variant import KlassVariantSearchByName
from .version import KlassVersion


class KlassClassification:
    """"In Klass a Classification can contain codes, versions and variants.
    Between Classifications Correspondances may exist.
    Classifications are identified by their classification_id.
    Print the Classification to see extensive information.

    To get at all the Classification's Variants (different aggregations of codelists), 
    you first need to get the classification at a specific time (a KlassVersion.)

    Parameters
    ----------
    classification_id : str
        The classification_id of the classification.
        For example: '36'
    language : str
        The language of the classification. "nb", "nn" or "en".
    include_future : bool
        Whether to include future versions of the classification.
        Default: False.

    Methods
    -------
    get_version()
        Returns a KlassVersion object of the classification based on ID. 
        If no ID is specified, will get the first version under the attribute .versions on this class.
    get_variant_by_name()
        Returns a KlassVariantSearchByName object by using this classification's classification_id,
        and a the start of a variant_name you specify.
    get_correspondance_to()
        Treats the current classification as a source of correspondances, you must specify the targets ID.
        Returns a KlassCorrespondance object of the correspondances.
    get_codes()
        Returns a KlassCodes object of the classification at a specific time, or in a specific time range.
    get_changes()
        Returns a KlassChanges object of the classification at a specific time, or in a specific time range.
        Different from get_codes() this method does not return all codes, 
        but only whats changed since last update, or within the time range.

    Attributes
    ----------
    versions : list
        A list of the data the Classifications has on its versions. 
        Versions represent the changes to the classifications codelists placed in time.
    name : str
        The name of the classification.
    classification_id : str
        The ID of the classification.
    classificationType : str
        The type of the classification.
    lastModified : str (ISO-datetime)
        The last time the classification was modified. ISO-stringified datetime
    description : str
        A longer description of the classification.
    primaryLanguage : str
        The primary language of the classification. "nb", "nn" or "en".
    language : str
        The language chosen at initialization of the classification. "nb", "nn" or "en".
    copyrighted : bool
        Whether the classification is copyrighted.
    includeShortName : bool
        If true, indicates that classificationItems may have shortnames.
    includeNotes : bool
        If true, indicates that classificationItems may have notes.
    contactPerson : dict
        A dictionary containing the contact person of the classification.
    owningSection : str
        The section (part of Statistics Norway)that owns the classification.
    statisticalUnits : list
        Statistical units assigned to classification
    include_future : bool
        Whether to include future versions of the classification.
    _links : dict
        A dictionary containing the links to different possible endpoints using the classification.

    Raises
    ------
    ValueError 
        If the language is not "no", "nb" or "en".
        If the include_future is not a bool.
    """
    def __init__(
        self, 
        classification_id: str, 
        language: str = "nb", 
        include_future: bool = False
    ):
        self.classification_id = classification_id
        self.language = language
        self.include_future = include_future

        for key, value in classification_by_id(
            classification_id, language=language, include_future=include_future
        ).items():
            setattr(self, key, value)

        version_replace = []
        for ver in self.versions:
            version_replace.append(
                {"version_id": int(ver["_links"]["self"]["href"].split("/")[-1]), **ver}
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
        if self.language != "nb":
            result += f"language='{self.language}', "
        if self.include_future:
            result += "include_future=True, "
        result += ")"
        return result

    def get_version(self,
                    version_id: int = 0,
                    select_level: int = 0, 
                    language: str = "", 
                    include_future: bool = None) -> KlassVersion:
        """Returns a KlassVersion object of the classification based on ID.
        A Version in Klass is a Classification placed in time.
        If no ID is specified, will get the first version under the attribute .versions on this class.
        
        Parameters
        ----------
        version_id : int
            The version ID of the version.
        select_level : int
            The level of the version to keep in the data.
        language : str
            The language of the version. "nn", "nb" or "en".
        include_future : bool
            Whether to include future versions of the version.
        
        Returns
        -------
        KlassVersion
            A KlassVersion object of the specified ID.
        
        Raises
        ------
        ValueError
            If the language is not "nn", "nb" or "en".
            If the include_future is not a bool.
        
        """
        if not version_id:
            version_id = self.versions[0]["version_id"]
        if language == "":
            language = self.language
        if include_future is None:
            include_future = self.include_future
        return KlassVersion(version_id, 
                            select_level=select_level, 
                            language=language, 
                            include_future=include_future)


    def get_variant_by_name(self,
                            name: str,
                            from_date: str,
                            to_date: str = "",
                            select_codes: str = "",
                            select_level: str = "",
                            presentation_name_pattern: str = "",
                            language: str = "nb",
                            include_future: bool = False) -> KlassVariantSearchByName:
        """Gets a KlassVariant by searching for its name, under the Variants owned by the current classification.
        
        In Klass a Variant is a different way of aggregating an existing codelist.
        It does not have to be extensive (all filled out), but can for example
        redefine upper levels, for some lower-level codes.

        Parameters
        ----------
        name : str
            The start of the name of the variant.
        from_date : str
            The start date of the time period.
        to_date : str
            The end date of the time period.
        select_codes : str
            Limit the result to codes matching this pattern. See rules: https://data.ssb.no/api/klass/v1/api-guide.html#_selectcodes
        select_level : str
            The level of the version to keep in the data.
        presentation_name_pattern : str
            Used to build an alternative presentation name for the codes. See rules: https://data.ssb.no/api/klass/v1/api-guide.html#_presentationnamepattern
        language : str
            The language of the version. "nn", "nb" or "en".
        include_future : bool
            Whether to include future versions of the version.

        Returns
        -------
        KlassVariantSearchByName
            A KlassVariantSearchByName object based on the classification's ID and searching for the name passed in.

        Raises
        ------
        ValueError
            If the language is not "nn", "nb" or "en".
            If the include_future is not a bool.
        """
        return KlassVariantSearchByName(classification_id=self.classification_id
                                        variant_name=name,
                                        from_date=from_date,
                                        to_date=to_date,
                                        select_codes=select_codes,
                                        select_level=select_level,
                                        presentation_name_pattern=presentation_name_pattern,
                                        language=language,
                                        include_future=include_future,
                                        )

    def get_correspondance_to(
        self,
        target_classification_id: str,
        from_date: str,
        to_date: str = "",
        language: str = "",
        include_future: bool = None,
    ) -> KlassCorrespondance:
        """Treats the current classification as a source of correspondances, you must specify the targets ID and a date.
        Returns a KlassCorrespondance object of the correspondances.
        
        Parameters
        ----------
        target_classification_id : str
            The classification ID of the target classification.
        from_date : str
            The start date of the time period.
        to_date : str
            The end date of the time period.
        language : str
            The language of the correspondances. "nn", "nb" or "en".
        include_future : bool
            Whether to include future correspondances.

        Returns
        -------
        KlassCorrespondance
            A KlassCorrespondance object of the correspondances between the current classification and the target classification.

        Raises
        ------
        ValueError
            If the language is not "nn", "nb" or "en".
            If the include_future is not a bool.
        
        """
        if language == "":
            language = self.language
        if include_future is None:
            include_future = self.include_future
        return KlassCorrespondance(
            source_classification_id=self.classification_id,
            target_classification_id=target_classification_id,
            from_date=from_date,
            to_date=to_date,
            language=language,
            include_future=include_future,
        )

    def get_codes(
        self,
        from_date: str = "",
        to_date: str = "",
        select_codes: str = "",
        select_level: str = "",
        presentation_name_pattern: str = "",
        language: str = "",
        include_future: bool = None,
    ) -> KlassCodes:
        """Returns a KlassCodes object of the classification at a specific time, or in a specific time range.
        
        Parameters
        ----------
        from_date : str
            The start date of the time period.
        to_date : str
            The end date of the time period.
        select_codes : str
            Limit the result to codes matching this pattern. See rules: https://data.ssb.no/api/klass/v1/api-guide.html#_selectcodes
        select_level : str
            The level of the version to keep in the data.
        presentation_name_pattern : str
            Used to build an alternative presentation name for the codes. See rules: https://data.ssb.no/api/klass/v1/api-guide.html#_presentationnamepattern
        language : str
            The language of the version. "nn", "nb" or "en".
        include_future : bool
            Whether to include future versions of the version.

        Returns
        -------
        KlassCodes
            A KlassCodes object of the classification at a specific time, or in a specific time range.

        """
        # If not passed to method, grab these from the Classification
        if language == "":
            language = self.language
        if include_future is None:
            include_future = self.include_future

        return KlassCodes(
            classification_id=self.classification_id,
            from_date=from_date,
            to_date=to_date,
            select_codes=select_codes,
            select_level=select_level,
            presentation_name_pattern=presentation_name_pattern,
            language=language,
            include_future=include_future,
        )

    def get_changes(
        self,
        from_date: str,
        to_date: str = "",
        language: str = "nb",
        include_future: bool = False,
    ) -> pd.DataFrame:
        """Returns a KlassChanges object of the classification at a specific time, or in a specific time range.
        Different from get_codes() this method does not return all codes, 
        but only whats changed since last update, or within the time range.
        
        Parameters
        ----------
        from_date : str
            The start date of the time period.
        to_date : str
            The end date of the time period.
        language : str
            The language of the version. "nn", "nb" or "en".
        include_future : bool
            Whether to include future versions of the version.

        Returns
        -------
        pd.DataFrame
            A pandas dataframe of the changes in the classification at a specific time (from last time it changed), 
            or within the specific time range.

        Raises
        ------
        ValueError
            If the language is not "nn", "nb" or "en".
            If the include_future is not a bool.
        """
        return changes(
            classification_id=self.classification_id,
            from_date=from_date,
            to_date=to_date,
            language=language,
            include_future=include_future,
        )
