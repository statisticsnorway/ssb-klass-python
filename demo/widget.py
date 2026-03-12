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

import klass

klass.__version__

# %%
from klass import search_classification

search_classification()

# %%
# Paste code here, after pression "copy code" button
from klass import KlassClassification

# %%
nus = KlassClassification(36)

# %%
nus_codes = nus.get_codes("2023-01-01")
display(nus_codes)

# %%
nus_codes.data.columns

# %%
display(nus_codes.pivot_level())

# %%
