# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.1
#   kernelspec:
#     display_name: ssb-klass-python
#     language: python
#     name: fake-stat-selvangivelse
# ---

# %%
from klass import KlassCorrespondence

# %%
KlassCorrespondence(correspondence_id="952", from_date="2020-12-31").to_dict(
    "sourceCode", "targetCode"
)

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
