# ssb-klass-python

A Python package built on top of KLASS's API for retrieving classifications, codes, correspondances etc.


## Example usage

```python
from klass import KlassClassification as KC # Import the class for KlassClassifications
nus = KC(36)  # Use ID for classification
codes = nus.get_codes() # codes from current date
print(codes)
codes.data  # Pandas dataframe available

```

```python
from klass import get_classification # Import the utility-function
nus = get_classification(36)

```


## Technical notes
Documentation for the [endpoints we are using can be found on Statistics Norways pages.](https://data.ssb.no/api/klass/v1/api-guide.html)

Technical architecture of the API we are interacting with is detailed in [Statistics Norway's internal wiki](https://wiki.ssb.no/display/KP/Teknisk+arkitektur#Tekniskarkitektur-GSIM).


---
