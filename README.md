# ssb-klass-python

A Python package built on top of Statistics Norway's code- and classification-system "KLASS". \
The package aims to make Klass's API for retrieving data easier to use by re-representing Klass's internal hierarchy as python-classes. Containing methods for easier traversal down, search classes and widgets, reasonable defaults to parameters etc.
Where data is possible to fit into pandas DataFrames, this will be preferred, but hirerachical data will be kept as json / dict structure.


## Example usages


```python
from klass import search_classification
# Opens a ipywidget in notebooks for searching for classifications and copying code, to get started
search_classification()  
```

```python
from klass import get_classification # Import the utility-function
nus = get_classification(36)
```

```python
# Does the same as the code above, but does not shy away from using the class directly
from klass import KlassClassification # Import the class for KlassClassifications
nus = KlassClassification(36)  # Use ID for classification
codes = nus.get_codes() # codes from current date
print(codes)
codes.data  # Pandas dataframe available under the .data attribute
```



## Technical notes
Documentation for the [endpoints we are using can be found on Statistics Norways pages.](https://data.ssb.no/api/klass/v1/api-guide.html)

Technical architecture of the API we are interacting with is detailed in [Statistics Norway's **internal** wiki](https://wiki.ssb.no/display/KP/Teknisk+arkitektur#Tekniskarkitektur-GSIM).


---
