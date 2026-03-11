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
from IPython.display import display

from klass import KlassSearchClassifications
from klass import KlassSearchFamilies

# %%
search = KlassSearchClassifications("land", no_dupes=True)
display(search)

# %%
display(search.get_classification(106))

# %%
ours = KlassSearchFamilies(360)
display(ours)

# %%
display(ours.families)

# %%
utdanning = ours.get_family(20)

# %%
display(utdanning)

# %%
isced = utdanning.get_classification(66)

# %%
display(isced)

# %%
