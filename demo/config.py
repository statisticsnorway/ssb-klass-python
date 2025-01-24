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
import klass

# %%
[x for x in dir(klass.config) if not x.startswith("_")]

# %%
klass.config.TESTING

# %%
klass.config.TESTING = True

# %%
klass.classification_by_id(36)

# %%
