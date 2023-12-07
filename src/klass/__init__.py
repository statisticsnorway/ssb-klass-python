"""A Python package built on top of Statistics Norway's code- and classification-system "KLASS".

The package aims to make Klass's API for retrieving data easier to use by re-representing Klass's internal hierarchy as python-classes.
Containing methods for easier traversal down, search classes and widgets, reasonable defaults to parameters etc.
Where data is possible to fit into pandas DataFrames, this will be preferred, but hirerachical data will be kept as json / dict structure.
"""

import importlib

import toml

# Gets the installed version from pyproject.toml, no need to update this file
try:
    __version__ = importlib.metadata.version("ssb-klass-python")
except importlib.metadata.PackageNotFoundError as e:
    try:
        __version__ = toml.load("../pyproject.toml")["tool"]["poetry"]["version"]
    except Exception as t:
        __version__ = "0.0.0"
        print(
            f"Error from ssb-klass-python not installed correctly(?) version unknown, setting it to {__version__}: {e} and {t}"
        )

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
