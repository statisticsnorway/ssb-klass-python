# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.6
#   kernelspec:
#     display_name: ssb-klass-python
#     language: python
#     name: ssb-klass-python
# ---

# %%
from klass import KlassSearchClassifications
from klass import KlassSearchFamilies

# %%
search = KlassSearchClassifications("land", no_dupes=True)
print(search)

# %%
print(search.get_classification(106))

# %%
ours = KlassSearchFamilies(360)
print(ours)

# %%
ours.families

# %%
utdanning = ours.get_family(20)

# %%
print(utdanning)

# %%
isced = utdanning.get_classification(66)

# %%
print(isced)

# %%
