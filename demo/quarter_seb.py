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

from klass import KlassCorrespondence

# %%
bydel = KlassCorrespondence(
    source_classification_id="1",
    target_classification_id="103",
    from_date="2020-01-01",
    contain_quarter=3,
)

# %%
display(bydel.from_date)

# %%
# Reset by parameter "contain_quarter" during initialization
display(bydel.to_date)

# %%
display(bydel.data)

# %%
display(bydel.data["validFrom"].min())

# %%
display(bydel.data["validTo"].max())

# %%
