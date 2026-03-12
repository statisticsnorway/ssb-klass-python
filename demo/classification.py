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

from klass import KlassClassification

# %%
# ID found from website: https://www.ssb.no/klass/
nus = KlassClassification(36, language="en", include_future=True)
display(nus)

# %%
display(repr(nus))

# %%
# Reformatting for fun
display(nus.versions_dict())

# %%
nuskoder = nus.get_codes("2023-01-01")
display(nuskoder)

# %%
display(nuskoder.pivot_level())

# %%
display(nuskoder.data)

# %%
# The actual data is under the .data attribute
display(nuskoder.data)

# %%
# Pivots levels into seperate columns
display(nuskoder.pivot_level())

# %%
# You can filter to a level when getting codes, and then make dict from that level
display(nus.get_codes("2023-01-01", select_level=5).to_dict())
