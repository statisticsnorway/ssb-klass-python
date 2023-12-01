"""The classes sub-module contains the actual classes the user should interact with.

They call loose get-request-functions in the requests-module under initialization.
Populating their attributes with metadata and data.
Traversing down through a hierarchy of Family > Classification > Version (classification at time) > Codelist is possible.
Traversing upwards is harder, as the API does not refer to parents of objects (would be nice if it did).
You can also traverse sideways to "correspondences" which exist as edge-objects between two classification-versions.
And get "variants", which are "alternative groupings" of codelists, belonging to versions.
"""
