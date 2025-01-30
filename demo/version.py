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
from klass import KlassVersion

# %%
nus2023 = KlassVersion("1954")
print(nus2023)

# %%
nus2023.variants_simple()

# %%
studiepoeng = nus2023.get_variant(1959)
print(studiepoeng)

# %%
{k: v["name"] for k, v in nus2023.correspondences_simple().items()}

# %%
nus_isced = nus2023.get_correspondence(1112)
print(nus_isced)

# %%
# Map directly from nus-code to isced-label using a dict, when specifying "other" you get a default-dict
nus_isced_map = nus_isced.to_dict(
    key="sourceCode", value="targetName", other="Unknown education programme"
)

# %%
nus_isced_map["899903"]

# %%
nus_isced_map["0"]

# %%
import pandas as pd

df = pd.DataFrame({"nus2000": ["099999", "899903"]})
df["isced_label"] = df["nus2000"].map(nus_isced_map)
df

# %%
