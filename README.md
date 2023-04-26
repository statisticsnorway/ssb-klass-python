# ssb-klass-python

A Python package built on top of KLASS's API for retrieving classifications, codes, correspondances etc.


## Example usage

```python
from klass import KlassClassification as kc # Import the class for KlassClassifications
nus = kc(36)  # Use ID for classification
codes = nus.get_codes() # codes from current date
print(codes)
codes.data  # Pandas dataframe available

```

```python
from klass import get_classification # Import the class for KlassClassifications
nus = get_classification(36)  # Use ID for classification
codes = nus.get_codes() # codes from current date
print(codes)
codes.data  # Pandas dataframe available

```


Technical architecture of the API we are interacting with is detailed in [Statistics Norway's internal wiki](https://wiki.ssb.no/display/KP/Teknisk+arkitektur#Tekniskarkitektur-GSIM).


---


