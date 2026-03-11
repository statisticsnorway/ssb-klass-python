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

# %%
klassifikasjoner = klass.classifications(
    include_codelists=True, changed_since="2022-01-01"
)

# %% [markdown]
# klassifikasjoner

# %%
display(klass.classification_by_id("36").keys())

# %%
display(
    klass.codes(classification_id="36", from_date="2020-01-01", to_date="2023-01-02")
)

# %% [raw]
#

# %%
display(klass.version_by_id("1954")["classificationVariants"])

# %%
# SELECT_LEVEL DOESNT WORK IN API?
display(
    klass.variant(
        "36",
        "Studiepoeng ved fagskole",
        "2023-01-01",
        # select_level=2,
        # return_type="json"
    )
)

# %%
display(klass.variant_at("36", "Studiepoeng ved fagskole", date="2022-01-01"))

# %%
display(klass.codes_at(classification_id="36", date="2023-01-01", language="en"))

# %%
display(
    klass.corresponds(
        source_classification_id=104,
        target_classification_id=131,
        from_date="2023-01-01",
        to_date="2024-01-01",
        language="en",
        include_future=True,
    )
)

# %%
display(
    klass.corresponds_at(
        source_classification_id=104,
        target_classification_id=131,
        date="2023-01-01",
    )
)

# %%
display(klass.correspondence_table_by_id("1111", language="en")["name"])

# %%
display(klass.changes("36", "2020-01-01", "2023-01-01"))

# %%
display(klass.classificationfamilies("360"))

# %%
display(klass.classificationfamilies_by_id(20))

# %%
