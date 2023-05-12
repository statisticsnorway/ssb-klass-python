import pytest
from unittest import mock
import requests

from klass import KlassConfig


def base_request(content: str, status_code: int = 200) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    response._content = bytes(content, "utf8",)
    response.request = requests.PreparedRequest()
    response.request.headers = KlassConfig().HEADERS
    return response


def classifications_mock():
    return base_request("""{'_embedded': {'classifications': [{'name': 'Standard for mocking tests',
    'classificationType': 'Klassifikasjon',
    'lastModified': '2023-04-18T12:56:21.000+0000',
    '_links': {'self': {'href': 'https://data.ssb.no/api/klass/v1/classifications/0'}}},
   ]},
 '_links': {'first': {'href': 'https://data.ssb.no/api/klass/v1/classifications?includeCodelists=false&page=0&size=20'},
  'self': {'href': 'https://data.ssb.no/api/klass/v1/classifications?includeCodelists=false'},
  'next': {'href': 'https://data.ssb.no/api/klass/v1/classifications?includeCodelists=false&page=0&size=20'},
  'last': {'href': 'https://data.ssb.no/api/klass/v1/classifications?includeCodelists=false&page=0&size=20'},
  'search': {'href': 'https://data.ssb.no/api/klass/v1/classifications/search{?query,includeCodelists}',
   'templated': True}},
 'page': {'size': 20, 'totalElements': 1, 'totalPages': 1, 'number': 0}}""")


def classification_search_mock():
    return base_request("""{'_embedded': {'searchResults': [{'name': 'Standard for mocking tests',
    'snippet': '<strong>1</strong> - Mann 2 - Kvinne',
    'searchScore': 1.1026883125305176,
    '_links': {'self': {'href': 'https://data.ssb.no/api/klass/v1/classifications/0'}}},]},
 '_links': {'first': {'href': 'https://data.ssb.no/api/klass/v1/classifications/search?query=1&includeCodelists=false&page=0&size=20'},
  'self': {'href': 'https://data.ssb.no/api/klass/v1/classifications/search?query=1&includeCodelists=false'},
  'next': {'href': 'https://data.ssb.no/api/klass/v1/classifications/search?query=1&includeCodelists=false&page=0&size=20'},
  'last': {'href': 'https://data.ssb.no/api/klass/v1/classifications/search?query=1&includeCodelists=false&page=0&size=20'}},
 'page': {'size': 20, 'totalElements': 1, 'totalPages': 1, 'number': 0}}""")


def classification_by_id_mock():
    return base_request("""{'name': 'Standard for mocking tests',
 'classificationType': 'Klassifikasjon',
 'lastModified': '2023-04-18T12:56:21.000+0000',
 'description': '',
 'primaryLanguage': 'en',
 'copyrighted': False,
 'includeShortName': False,
 'includeNotes': True,
 'contactPerson': {'name': 'SSB Pythonistas',
  'email': 'pythonistas@ssb.no',
  'phone': '99999999'},
 'owningSection': '320 - Seksjon for befolkningsstatistikk',
 'statisticalUnits': ['Mock'],
 'versions': [{'name': 'Mock Version',
   'validFrom': '2016-01-01',
   'validTo': '2050-01-01',
   'lastModified': '2023-04-18T12:43:39.000+0000',
   'published': ['en'],
   '_links': {'self': {'href': 'https://data.ssb.no/api/klass/v1/versions/0'}}},,],
 '_links': {'self': {'href': 'https://data.ssb.no/api/klass/v1/classifications/0'},
  'codes': {'href': 'https://data.ssb.no/api/klass/v1/classifications/0/codes{?from=<yyyy-MM-dd>,to=<yyyy-MM-dd>,csvSeparator,level,selectCodes,presentationNamePattern}',
   'templated': True},
  'codesAt': {'href': 'https://data.ssb.no/api/klass/v1/classifications/0/codesAt{?date=<yyyy-MM-dd>,csvSeparator,level,selectCodes,presentationNamePattern}',
   'templated': True},
  'variant': {'href': 'https://data.ssb.no/api/klass/v1/classifications/0/variant{?variantName,from=<yyyy-MM-dd>,to=<yyyy-MM-dd>,csvSeparator,level,selectCodes,presentationNamePattern}',
   'templated': True},
  'variantAt': {'href': 'https://data.ssb.no/api/klass/v1/classifications/0/variantAt{?variantName,date=<yyyy-MM-dd>,csvSeparator,level,selectCodes,presentationNamePattern}',
   'templated': True},
  'corresponds': {'href': 'https://data.ssb.no/api/klass/v1/classifications/0/corresponds{?targetClassificationId,from=<yyyy-MM-dd>,to=<yyyy-MM-dd>,csvSeparator}',
   'templated': True},
  'correspondsAt': {'href': 'https://data.ssb.no/api/klass/v1/classifications/0/correspondsAt{?targetClassificationId,date=<yyyy-MM-dd>,csvSeparator}',
   'templated': True},
  'changes': {'href': 'https://data.ssb.no/api/klass/v1/classifications/0/changes{?from=<yyyy-MM-dd>,to=<yyyy-MM-dd>,csvSeparator}',
   'templated': True}}}""")


def codes_mock():
    return base_request("")


def codes_at_mock():
    return base_request("")


def version_by_id_mock():
    return base_request("")


def variant_mock():
    return base_request("")


def variant_at_mock():
    return base_request("")


def variants_by_id_mock():
    return base_request("")


def corresponds_mock():
    return base_request("")


def corresponds_at_mock():
    return base_request("")


def correspondance_table_by_id_mock():
    return base_request("")


def changes_mock():
    return base_request("")


def classificationfamilies_mock():
    return base_request("")


def classificationfamilies_by_id_mock():
    return base_request("")


def sections_list_mock():
    return base_request("")