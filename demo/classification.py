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
from klass import KlassClassification

# %%
# ID found from website: https://www.ssb.no/klass/
nus = KlassClassification(36, language="en", include_future=True)
print(nus)

# %%
repr(nus)

# %%
# Reformatting for fun
nus.versions_dict()

# %%
nuskoder = nus.get_codes("2023-01-01")
print(nuskoder)

# %%
nuskoder.pivot_level()

# %%
nuskoder.data

# %%
# The actual data is under the .data attribute
nuskoder.data

# %%
# Pivots levels into seperate columns
nuskoder.pivot_level()

# %%
# You can filter to a level when getting codes, and then make dict from that level
nus.get_codes("2023-01-01", select_level=5).to_dict()
