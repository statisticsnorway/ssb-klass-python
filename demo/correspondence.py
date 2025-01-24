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
from klass import KlassCorrespondence

# %%
fylke_komm = KlassCorrespondence(
    source_classification_id="131",
    target_classification_id="104",
    from_date="2023-01-01",
)

# %%
print(fylke_komm)

# %%
fylke_komm.data

# %%
fylke_komm.to_dict("sourceName", "targetName")
