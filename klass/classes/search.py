from ..requests.klass_requests import classification_search, classificationfamilies
from .classification import KlassClassification
from .family import KlassFamily


class KlassSearchClassifications:
    """Used to search for classifications.

    Parameters
    ----------
    query: str
        The search query.
    include_codelists: bool
        Whether to include codelists in the search results.
    ssbsection: str
        The SSB section who owns the classification you are seraching for.
    no_dupes: bool
        Whether to remove duplicates from the search results.
        (Usually caused by languages showing up multiple times)


    Attributes
    ----------
    classifications: list
        A list of KlassClassification objects.

    query: str
        The search query.
    include_codelists: bool
        Whether to include codelists in the search results.
    ssbsection: str
        The SSB section who owns the classification you are seraching for.
    no_dupes: bool
        Whether to remove duplicates from the search results.


    Methods
    -------
    get_search()
        Searches for classifications. Run as last part of initialization.
        Rerun this method, if you change any of the parameters on the object.
    simple_search_result()
        Returns a simple string of the classifications.
    get_classification()
        Convenience-method for getting a Classification from the search object.
    """

    def __init__(
        self,
        query: str = "",
        include_codelists: bool = True,  # Opposite default of API, cause why not
        ssbsection: str = "",
        no_dupes=False,
    ):
        self.query = query
        self.include_codelists = include_codelists
        self.ssbsection = ssbsection
        self.no_dupes = no_dupes
        self.get_search()

    def get_search(self) -> None:
        # If you enter a number, replace with name of the classification
        if self.query.isdigit() and self.query != "":
            result = KlassClassification(self.query)
            print(result.name)
            self.query = "".join([c for c in result.name if c.isalnum() or c == " "])
        elif not self.query and self.ssbsection:
            self.query = " "

        result = classification_search(
            query=self.query,
            include_codelists=self.include_codelists,
            ssbsection=self.ssbsection,
        )
        if "_embedded" in result.keys():
            self.classifications = result["_embedded"]["searchResults"]
        elif "searchResults" in result.keys():
            self.classifications = result["searchResults"]
        else:
            self.classifications = []

        self.links = result["_links"]
        if len(self.classifications):
            classification_replace = []
            for cl in self.classifications:
                cl = {
                    "classification_id": int(
                        cl["_links"]["self"]["href"].split("/")[-1]
                    ),
                    **cl,
                }
                classification_replace.append(cl)
            self.classifications = classification_replace
            if self.no_dupes:
                classification_replace = []
                seen = []
                for cl in self.classifications:
                    if cl["classification_id"] not in seen:
                        classification_replace.append(cl)
                        seen.append(cl["classification_id"])
                self.classifications = classification_replace

    def __str__(self) -> str:
        classifications_string = "\n\t".join(
            [
                ": ".join([str(c["classification_id"]), c["name"]])
                for c in self.classifications
            ]
        )
        return f"""The search for "{self.query}" returned the following classifications:
        {classifications_string}"""

    def __repr__(self) -> str:
        result = f'KlassSearchClassifications(query="{self.query}", '
        if not self.include_codelists:
            result += f'include_codelists="{self.include_codelists}", '
        if self.ssbsection:
            result += f'ssbsection="{self.ssbsection}", '
        if self.no_dupes:
            result += f"no_dupes={self.no_dupes}"
        result += ")"
        return result

    @staticmethod
    def get_classification(
        classification_id: str, language: str = "nb", include_future: bool = False
    ) -> KlassClassification:
        """Convenience-method for getting a Classification from the search object.

        Parameters
        ----------
        classification_id : str
            The classification ID to get.
        language : str
            The language to get the classification in.
            Default: "nb" for Norwegian, "nn" for Nynorsk, "en" for English.
        include_future : bool
            Whether to include future codelists.

        Returns
        -------
        KlassClassification
            The classification object.

        """
        return KlassClassification(classification_id, language, include_future)

    def simple_search_result(self) -> str:
        """Reformats the resulting search into a simple string.

        Returns
        -------
        str
            The resulting reformatted string from the search results

        """
        result = ""
        if len(self.classifications):
            for cl in self.classifications:
                result += f'{cl["classification_id"]}: {cl["name"]}\n'
        else:
            result = "Found no classifications"
        return result


class KlassSearchFamilies:
    """Used for searching for families in the Klass API.

    Parameters
    ----------
    ssbsection : str
        The SSB section who owns the family you are searching for.
    include_codelists : bool
        Whether to include codelists in the search.
    language : str
        The language to use in the search.
        Default: "nb" for Norwegian, "nn" for Nynorsk, "en" for English.

    Methods
    -------
    get_search()
        Runs the search. Rerun this if you change any attributes on the object.
    get_family()
        Returns a KlassFamily object of the family with the given ID.
    simple_search_result()
        Returns a simple string of the search results.
    """

    def __init__(
        self,
        ssbsection: str = "",
        include_codelists: bool = False,
        language: str = "nb",
    ):
        self.ssbsection = ssbsection
        self.include_codelists = include_codelists
        self.language = language
        self.get_search()

    def __str__(self) -> str:
        result = ""
        for fam in self.families:
            result += f"Family ID: {fam['family_id']} - {fam['name']} - "
            result += f"Number of classifications: {fam['numberOfClassifications']}\n"
        return result

    def __repr__(self) -> str:
        result = "KlassSearchFamilies("
        if self.ssbsection:
            result += f'ssbsection="{self.ssbsection}", '
        if self.include_codelists:
            result += f"include_codelists={self.include_codelists}, "
        if self.language != "nb":
            result += f'language="{self.language}"'
        result += ")"
        return result

    def get_search(self) -> None:
        """Gets the search result from the API and reformats it into the .families and .links attributes.
        This should be run after any change to the .ssbsection, .include_codelists, or .language
        attributes.

        Returns
        -------
        None
            Sets .families and .links attributes.

        """
        result = classificationfamilies(
            ssbsection=self.ssbsection,
            include_codelists=self.include_codelists,
            language=self.language,
        )
        self.families = result["_embedded"]["classificationFamilies"]
        self.links = result["_links"]
        families_replace = []
        for fam in self.families:
            fam["family_id"] = int(fam["_links"]["self"]["href"].split("/")[-1])
            families_replace.append(fam)
        self.families = families_replace

    def get_family(self, family_id=0) -> KlassFamily:
        """Returns a KlassFamily object of the family with the given ID.
        If no ID is given, chooses the first Family returned by the search.

        Parameters
        ----------
        family_id : int
            The family ID to get.

        Returns
        -------
        KlassFamily
            The family object.

        """
        if not family_id:
            family_id = self.families[0]["family_id"]
        return KlassFamily(family_id)

    def simple_search_result(self) -> str:
        """Reformats the resulting search into a simple string.

        Returns
        -------
        str
            The resulting reformatted string from the search results

        """
        result = ""
        for fl in self.families:
            result += f'ID {fl["family_id"]} - {fl["name"]}: '
            result += f'Contains {fl["numberOfClassifications"]} Classifications\n'
        return result
