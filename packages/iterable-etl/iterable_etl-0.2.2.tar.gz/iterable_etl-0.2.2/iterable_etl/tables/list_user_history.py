"""list_user_history"""
import time
from typing import Any, Dict, List

import pandas as pd
from pandas import DataFrame as PandasDF

from iterable_etl.libs.cnst import get_headers, urls
from iterable_etl.libs.dbg import (
    dbg,
    error_handler_decorator,
    print_dataframe_head,
    write_dataframe_to_csv,
)
from iterable_etl.libs.network import get_data_json, get_data_text
from iterable_etl.libs.transform import csv_to_dataframe


def get_list_ids(api_url: str, headers: Dict[str, str]) -> List[Any]:
    """Make a GET request to the Iterable API and return a dictionary of list data."""
    data = get_data_json(api_url, headers)
    list_ids = [_list["id"] for _list in data["lists"]]
    list_ids.sort()
    return list_ids


def default_diff_writer():
    dbg("no diff writer")


# spark: SparkSession, pandas_df: PandasDF, target_schema_table_name: str


@write_dataframe_to_csv("list_user_history")
@print_dataframe_head
@error_handler_decorator
def list_user_history_df(
    spark=None, target_schema_table_name=None, diff_writer=None
) -> PandasDF:
    """
    list_user_history dataframe

    This will take ~12 hours to run. It should be setup as an individual job.

    TODO: Further diffing work to make the run less jank.

    """

    list_user_history_url = urls["lists_get_users"]

    df = pd.DataFrame()

    list_ids = get_list_ids(urls["lists"], get_headers())

    for i, list_id in enumerate(list_ids):
        dbg(
            "user list for list id {} of {}, list_id= {}".format(
                i, len(list_ids), list_id
            )
        )
        url = f"{list_user_history_url}{list_id}"

        response_text = get_data_text(url, get_headers())

        time.sleep(13)

        if response_text:
            dbg("list_id={} has content".format(list_id))
            _df = csv_to_dataframe(response_text)
            _df = _df.rename(columns={_df.columns[0]: "user_email"})
            _df["list_id"] = list_id
            if (
                spark is not None
                and target_schema_table_name is not None
                and diff_writer is not None
                and _df.shape[0] > 0
            ):
                diff_writer(spark, _df, target_schema_table_name)
            df = pd.concat([df, _df])

    return df
