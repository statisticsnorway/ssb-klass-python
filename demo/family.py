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

from klass import KlassSearchFamilies

# %%
search = KlassSearchFamilies("360")
display(search)

# %%
utdanning = search.get_family(20)
display(utdanning)

# %%
nus = utdanning.get_classification(36)
display(nus)

# %%
nus_codes = nus.get_codes("2023-01-01")
display(nus_codes)

# %%
display(nus_codes.data)

# %%
