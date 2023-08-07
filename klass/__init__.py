from importlib import import_module


__version__ = "0.0.4"
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
        "correspondance_table_by_id",
        "changes",
        "classificationfamilies",
        "classificationfamilies_by_id",
    ],
    "classes.codes": ["KlassCodes"],
    "classes.correspondance": ["KlassCorrespondance"],
    "classes.classification": ["KlassClassification"],
    "classes.family": ["KlassFamily"],
    "classes.search": ["KlassSearchClassifications", "KlassSearchFamilies"],
    "requests.sections": ["sections_list", "sections_dict"],
    "classes.variant": ["KlassVariant", "KlassVariantSearchByName"],
    "classes.version": ["KlassVersion"],
    "utility.codes": ["get_codes"],
    "utility.classification": ["get_classification"],
    "widgets.search_ipywidget": ["search_classification"],
    "klass_config": ["KlassConfig"],
}

# Loop that imports local files into this namespace and appends to __all__ for star imports
for file, funcs in local_imports.items():
    for func in funcs:
        globals()[func] = getattr(import_module(f"klass.{file}", func), func)
        __all__.append(func)
