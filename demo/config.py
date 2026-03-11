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
import klass.config

# %%
[x for x in dir(klass.config) if not x.startswith("_")]

# %%
display(klass.config.TESTING)

# %%
klass.config.TESTING = True

# %%
display(klass.classification_by_id(36))

# %%
