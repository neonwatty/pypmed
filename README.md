[![Python application](https://github.com/jermwatt/pypmed/actions/workflows/python-app.yml/badge.svg)](https://github.com/jermwatt/pypmed/actions/workflows/python-app.yml)

# pypmed - a simple Python interface for [PubMed's API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi/)

pypmed is a Python library that provides easy access to the [PubMed's APIs](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi/).

## Installation

`pip install pypmed`

## Example usage

This example can be executed in [this example notebook](https://colab.research.google.com/github/jermwatt/pynih/blob/main/pynih_example_usage.ipynb#scrollTo=mTC2IDzs7_l1).

```python
from pypmed import apis 

search_criteria = {'author_first_name': 'rachel', 
                   'author_last_name': 'gottschalk', 
                   'institution':  'university of pittsburgh at pittsburgh',
                   'publication_year': 2022
                   }

response = apis.query_pubmed_api(search_criteria=search_criteria)
```
