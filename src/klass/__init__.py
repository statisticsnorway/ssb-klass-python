"""A Python package built on top of Statistics Norway's code- and classification-system "KLASS".

The package aims to make Klass's API for retrieving data easier to use by re-representing Klass's internal hierarchy as python-classes.
Containing methods for easier traversal down, search classes and widgets, reasonable defaults to parameters etc.
Where data is possible to fit into pandas DataFrames, this will be preferred, but hirerachical data will be kept as json / dict structure.
"""

import importlib

import toml


# Split into function for testing
def _try_getting_pyproject_toml(e: Exception | None = None) -> str:
    if e is None:
        passed_excep: Exception = Exception("")
    else:
        passed_excep = e
    try:
        version: str = toml.load("../pyproject.toml")["tool"]["poetry"]["version"]
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


__all__ = []

# Everything we want to be directly importable from under "klass"-package
local_imports = {
    "requests.klass_requests": [
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
    ],
    "classes.codes": ["KlassCodes"],
    "classes.correspondence": ["KlassCorrespondence"],
    "classes.classification": ["KlassClassification"],
    "classes.family": ["KlassFamily"],
    "classes.search": ["KlassSearchClassifications", "KlassSearchFamilies"],
    "requests.sections": ["sections_list", "sections_dict"],
    "classes.variant": ["KlassVariant", "KlassVariantSearchByName"],
    "classes.version": ["KlassVersion"],
    "utility.codes": ["get_codes"],
    "utility.classification": ["get_classification"],
    "widgets.search_ipywidget": ["search_classification"],
}

# Loop that imports local files into this namespace and appends to __all__ for star imports
for file, funcs in local_imports.items():
    for func in funcs:
        globals()[func] = getattr(importlib.import_module(f"klass.{file}", func), func)
        __all__.append(func)
