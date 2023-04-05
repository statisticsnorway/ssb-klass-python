import requests
import pandas as pd
import dateutil.parser
from datetime import timezone, timedelta

from ..klass_config import BASE_URL, HEADERS
from .validate import validate_params
from .sections import sections_dict

# ##########
# GENERAL #
# ##########


def get_json(url, params):
    req = requests.Request("GET", url=url, headers=HEADERS, params=params)
    #print(req.url, req.headers, req.params)
    print("Full URL, check during testing:", req.prepare().url)
    response = requests.Session().send(req.prepare())
    response.raise_for_status()
    #print(response.text)
    return response.json()


def convert_return_type(data, return_type="pandas"):
    if return_type == "json":
        return data
    return pd.json_normalize(data)


def convert_datestring(date: str, return_type = "isoklass") -> str:
    date = dateutil.parser.parse(date)
    date = date.replace(tzinfo=timezone(timedelta(hours=1)))
    if return_type == "isoklass":
        return date.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + date.strftime("%z")
    elif return_type == "yyyy-mm-dd":
        return date.strftime("%Y-%m-%d")
    raise ValueError("Unrecognized datetimestring return type")


def convert_section(section: str) -> str:
    if " " not in str(section):
        return sections_dict()[str(section)]
    return section

# ############
# ENDPOINTS #
# ############


def classifications(include_codelists: bool = False,
                    changed_since: str = ""):
    url = BASE_URL + "classifications"
    params = {'includeCodelists': include_codelists, }
    if changed_since:
        params["changedSince"] = convert_datestring(changed_since, "isoklass")
    params = validate_params(params)
    return get_json(url, params)


def classification_search(query: str = "",
                          include_codelists: bool = False,
                          ssbsection: str = ""):
    url = BASE_URL + "classifications/search"
    if not query:
        raise ValueError("Please specify a query")
    params = {'query': query, 'includeCodelists': include_codelists, }
    if ssbsection:
        params['ssbSection'] = convert_section(ssbsection)
    params = validate_params(params)
    return get_json(url, params)


def classification_by_id(classification_id: str,
                         language: str = 'nb', 
                         include_future: bool = False,
                         return_type: str = "json") -> dict:
    url = BASE_URL + "classifications/" + str(classification_id)
    params = validate_params({'language': language,
                              'includeFuture': include_future})
    return convert_return_type(get_json(url, params), return_type)


def codes(classification_id: str,
          from_date: str,
          to_date: str = "",
          select_codes: str = "",
          select_level: str = "",
          presentation_name_pattern: str = "",
          language: str = "nb",
          include_future: bool = False,
          return_type: str = "pandas",
          wide: bool = False
         ) -> pd.DataFrame:
    url = BASE_URL + "classifications/" + str(classification_id) + "/codes"
    from_date = convert_datestring(from_date, "yyyy-mm-dd")
    params = {
        'from': from_date,
        'selectCodes': select_codes,
        'selectLevel': select_level,
        'presentationNamePattern': presentation_name_pattern,
        'language': language,
        'includeFuture': include_future,
    }
    if to_date:
        params["to"] = convert_datestring(to_date)
        params["to"] = to_date
    params = validate_params({k: v for k, v in params.items() if v != ""})
    df_long = convert_return_type(get_json(url, params)["codes"], return_type)
    if wide: return to_wide(df_long)
    else: return df_long


def codes_at(classification_id: str,
             date: str,
             select_codes: str = "",
             select_level: str = "",
             presentation_name_pattern: str = "",
             language: str = "nb",
             include_future: bool = False,
             return_type: str = "pandas",
             wide: bool = False
             ):
    url = BASE_URL + "classifications/" + str(classification_id) + "/codesAt"
    date = convert_datestring(date, "yyyy-mm-dd")
    params = {
        'date': date,
        'selectCodes': select_codes,
        'selectLevel': select_level,
        'presentationNamePattern': presentation_name_pattern,
        'language': language,
        'includeFuture': include_future,
    }
    params = validate_params({k: v for k, v in params.items() if v != ""})
    df_long = convert_return_type(get_json(url, params)["codes"], return_type)
    if wide: return to_wide(df_long)
    else: return df_long


def to_wide(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    This function converts from long to wide data format. The level codes are
    preserved in the column names. Use this to get a dataframe where all rows
    are entries in the highest levels.
    """
    
    df_raw = df_raw[['code', 'parentCode', 'level', 'name']]
    
    lowest_level = int(df_raw.level.unique().max())
    df_list = []
    for i in range(1, lowest_level+1):
        temp = df_raw[df_raw['level'] == f'{i}'].copy()
        temp.columns = [f'code_{i}', f'parentCode_{i}', 'level', f'name_{i}']
        temp = temp.drop(columns=['level'])
        df_list.append(temp)
    df_wide = df_list[0].copy()

    for i in range(0, len(df_list)-1):
        this_lvl = i + 1
        child_lvl = i + 2

        df_wide = pd.merge(
             df_wide,
             df_list[i+1],
             how='left',
             left_on=f'code_{this_lvl}',
             right_on=f'parentCode_{child_lvl}'
        )
    return df_wide


def version_by_id(version_id: str,
                  language: str = "nb",
                  include_future: bool = False,
                  return_type: str = "json"):
    url = BASE_URL + "versions/" + str(version_id)
    params = validate_params({
        'language': language,
        'includeFuture': include_future,
    })
    return convert_return_type(get_json(url, params), return_type)


def variant(classification_id: str,
            variant_name: str,
            from_date: str,
            to_date: str = "",
            select_codes: str = "",
            select_level: str = "",
            presentation_name_pattern: str = "",
            language: str = "nb",
            include_future: bool = False,
            return_type: str = "pandas"):
    url = BASE_URL + "classifications/" + str(classification_id) + "/variant"
    from_date = convert_datestring(from_date, "yyyy-mm-dd")
    params = {
        'variantName': variant_name,
        'from': from_date,
        #'to': to_date,
        'selectCodes': select_codes,
        'selectLevel': select_level,
        'presentationNamePattern': presentation_name_pattern,
        'language': language,
        'includeFuture': include_future,
    }
    if to_date:
        params["to"] = convert_datestring(to_date, "yyyy-mm-dd")
    params = validate_params({k: v for k, v in params.items() if v != ""})
    print(params)
    return convert_return_type(get_json(url, params), return_type)


def variant_at(classification_id: str,
               variant_name: str,
               date: str,
               select_codes: str = "",
               select_level: str = "",
               presentation_name_pattern: str = "",
               language: str = "nb",
               include_future: bool = False,
               return_type: str = "pandas"):
    url = BASE_URL + "classifications/" + str(classification_id) + "/variantAt"
    date = convert_datestring(date, "yyyy-mm-dd")
    params = {
        'variantName': variant_name,
        'date': date,
        'selectCodes': select_codes,
        'selectLevel': select_level,
        'presentationNamePattern': presentation_name_pattern,
        'language': language,
        'includeFuture': include_future,
    }
    params = validate_params({k: v for k, v in params.items() if v != ""})
    return convert_return_type(get_json(url, params), return_type)


def variants_by_id(variant_id: str,
                  language: str = "nb",
                  return_type: str = "json"
                  ):
    url = BASE_URL + "variants/" + str(variant_id)
    params = validate_params({'language': language})
    return convert_return_type(get_json(url, params), return_type)


def corresponds(source_classification_id: str,
                target_classification_id: str,
                from_date: str,
                to_date: str = "",
                language: str = "nb",
                include_future: bool = False,
                return_type: str = "pandas"):
    url = BASE_URL + "classifications/" + str(source_classification_id) + "/corresponds"
    from_date = convert_datestring(from_date, "yyyy-mm-dd")
    params = {
        'targetClassificationId': target_classification_id,
        'from': from_date,
        #'to': to_date,
        'language': language,
        'includeFuture': include_future,
    }
    if to_date:
        params["to"] = convert_datestring(to_date, "yyyy-mm-dd")
    params = validate_params({k: v for k, v in params.items() if v != ""})
    return convert_return_type(get_json(url, params)['correspondenceItems'], return_type)


def corresponds_at(source_classification_id: str,
                   target_classification_id: str,
                   date: str,
                   language: str = "nb",
                   include_future: bool = False,
                   return_type: str = "pandas"):
    url = BASE_URL + "classifications/" + str(source_classification_id) + "/correspondsAt"
    date = convert_datestring(date, "yyyy-mm-dd")
    params = {
        'targetClassificationId': target_classification_id,
        'date': date,
        'language': language,
        'includeFuture': include_future,
    }
    params = validate_params({k: v for k, v in params.items() if v != ""})
    return convert_return_type(get_json(url, params)['correspondenceItems'], return_type)


def correspondance_table_by_id(correspondance_id: str,
                               language: str = "nb",
                               return_type: str = "json"):
    url = BASE_URL + "correspondencetables/" + str(correspondance_id)
    params = validate_params({'language': language})
    return convert_return_type(get_json(url, params), return_type)


def changes(classification_id: str,
            from_date: str,
            to_date: str = "",
            language: str = "nb",
            include_future: bool = False,
            return_type: str = "pandas"
           ):
    url = BASE_URL + "classifications/" + str(classification_id) + "/changes"
    from_date = convert_datestring(from_date, "yyyy-mm-dd")
    to_date = convert_datestring(to_date, "yyyy-mm-dd")
    params = {
        'from': from_date,
        'to': to_date,
        'language': language,
        'includeFuture': include_future,
    }
    params = validate_params({k: v for k, v in params.items() if v != ""})
    return convert_return_type(get_json(url, params)['codeChanges'], return_type)


def classificationfamilies(ssbsection: str = "",
                           include_codelists: bool = False,
                           language: str = "nb",
                           ):
    url = BASE_URL + "classificationfamilies"
    params = {'includeCodelists': include_codelists, 'language': language}
    if ssbsection:
        params['ssbSection'] = convert_section(ssbsection)
    params = validate_params(params)
    return get_json(url, params)


def classificationfamilies_by_id(classificationfamily_id: str,
                                 ssbsection: str = "",
                                 include_codelists: bool = False,
                                 language: str = "nb",):
    url = BASE_URL + "classificationfamilies/" + str(classificationfamily_id)
    params = {'includeCodelists': include_codelists, 'language': language}
    if ssbsection:
        params['ssbSection'] = convert_section(ssbsection)
    params = validate_params(params)
    return get_json(url, params)
