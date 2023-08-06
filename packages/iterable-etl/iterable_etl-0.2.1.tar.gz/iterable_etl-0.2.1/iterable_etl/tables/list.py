"""list"""

from typing import Any, Dict

from pandas import DataFrame as PandasDF

from iterable_etl.libs.cnst import get_headers, urls
from iterable_etl.libs.dbg import print_dataframe_head, write_dataframe_to_csv
from iterable_etl.libs.network import get_data_json
from iterable_etl.libs.transform import json_to_dataframe


def get_list_data(api_url: str, headers: Dict[str, str]) -> Dict[str, Any]:
    """Make a GET request to the Iterable API and return a dictionary of list data."""
    data = get_data_json(api_url, headers)
    return data["lists"]


@write_dataframe_to_csv("list")
@print_dataframe_head
def list_df() -> PandasDF:
    """list dataframe"""
    data = get_list_data(urls["lists"], get_headers())
    df = json_to_dataframe(data)
    return df
