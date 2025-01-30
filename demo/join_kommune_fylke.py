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
import pandas as pd

from klass import KlassClassification

# %%
kom = (
    KlassClassification("131")
    .get_codes(from_date="2022-01-01")
    .data[["code", "name"]]
    .rename(columns={"code": "kommunenummer", "name": "kommune"})
)
fyl = (
    KlassClassification("104")
    .get_codes(from_date="2022-01-01")
    .data[["code", "name"]]
    .rename(columns={"code": "fylkesnummer", "name": "fylke"})
)

# %%
kom["fylkesnummer"] = kom["kommunenummer"].str[:2]
komfyl = pd.merge(kom, fyl, how="left", on="fylkesnummer")
komfyl

# %%
