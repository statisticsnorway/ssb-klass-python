"""A Python package built on top of Statistics Norway's code- and classification-system "KLASS".

The package aims to make Klass's API for retrieving data easier to use by re-representing Klass's internal hierarchy as python-classes.
Containing methods for easier traversal down, search classes and widgets, reasonable defaults to parameters etc.
Where data is possible to fit into pandas DataFrames, this will be preferred, but hirerachical data will be kept as json / dict structure.
"""

import importlib
import importlib.metadata

import toml


def _try_getting_pyproject_toml(e: Exception | None = None) -> str:
    if e is None:
        passed_excep: Exception = Exception("")
    else:
        passed_excep = e
    try:
        version: str = toml.load("pyproject.toml")["tool"]["poetry"]["version"]
        return version
    except Exception as e:
        version_missing: str = "0.0.0"
        print(
            f"Error from ssb-klass-pythons __init__, not able to get version-number, setting it to {version_missing}: {passed_excep}"
        )
        return version_missing


# Gets the installed version from pyproject.toml, then there is no need to update this file
try:
    __version__ = importlib.metadata.version("ssb-klass-python")
except importlib.metadata.PackageNotFoundError as e:
    __version__ = _try_getting_pyproject_toml(e)


from klass.classes.classification import KlassClassification
from klass.classes.codes import KlassCodes
from klass.classes.correspondence import KlassCorrespondence
from klass.classes.family import KlassFamily
from klass.classes.search import KlassSearchClassifications
from klass.classes.search import KlassSearchFamilies
from klass.classes.variant import KlassVariant
from klass.classes.variant import KlassVariantSearchByName
from klass.classes.version import KlassVersion
from klass.requests.klass_requests import changes
from klass.requests.klass_requests import classification_by_id
from klass.requests.klass_requests import classification_search
from klass.requests.klass_requests import classificationfamilies
from klass.requests.klass_requests import classificationfamilies_by_id
from klass.requests.klass_requests import classifications
from klass.requests.klass_requests import codes
from klass.requests.klass_requests import codes_at
from klass.requests.klass_requests import correspondence_table_by_id
from klass.requests.klass_requests import corresponds
from klass.requests.klass_requests import corresponds_at
from klass.requests.klass_requests import variant
from klass.requests.klass_requests import variant_at
from klass.requests.klass_requests import variants_by_id
from klass.requests.klass_requests import version_by_id
from klass.requests.sections import sections_dict
from klass.requests.sections import sections_list
from klass.utility.classification import get_classification
from klass.utility.codes import get_codes
from klass.widgets.search_ipywidget import search_classification

__all__ = [
    "classifications",
    "classification_search",
    "classification_by_id",
    "codes",
    "codes_at",
    "version_by_id",
    "variant",
    "variant_at",
    "variants_by_id",
    "corresponds",
    "corresponds_at",
    "correspondence_table_by_id",
    "changes",
    "classificationfamilies",
    "classificationfamilies_by_id",
    "sections_list",
    "sections_dict",
    "KlassCodes",
    "KlassCorrespondence",
    "KlassClassification",
    "KlassFamily",
    "KlassSearchClassifications",
    "KlassSearchFamilies",
    "KlassVariant",
    "KlassVariantSearchByName",
    "KlassVersion",
    "get_codes",
    "get_classification",
    "search_classification",
]
