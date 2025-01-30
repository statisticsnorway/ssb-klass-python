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
from klass import KlassVariant
from klass import KlassVariantSearchByName

# %%
studpoeng = KlassVariantSearchByName(36, "Studiepoeng ved fagskole", "2023-01-01")

# %%
print(studpoeng)

# %%
studpoeng.get_variant()

# %%
studpoeng2 = KlassVariant(1959)
print(studpoeng2)

# %%
studpoeng2.data
