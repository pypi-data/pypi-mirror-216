"""user_history"""

from typing import Dict
from datetime import datetime

from pandas import DataFrame as PandasDF

from iterable_etl.libs.cnst import get_headers, urls
from iterable_etl.libs.dbg import print_dataframe_head, write_dataframe_to_csv
from iterable_etl.libs.network import get_data_csv
from iterable_etl.libs.transform import csv_to_dataframe


def get_export_data(api_url: str, headers: Dict[str, str]) -> str:
    """Make a GET request to the Iterable API and return a csv string of export data."""
    data = get_data_csv(api_url, headers)
    return data


def create_only_fields(onlyFields: str) -> str:
    string = "&".join(f"onlyFields={field}" for field in onlyFields)
    return string


@write_dataframe_to_csv("user_history")
@print_dataframe_head
def user_history_df(
    start_date: str,
    end_date: str,
    fields_list=[
        "email",
        "emailListIds",
        "firstName",
        "lastName",
        "phoneNumber",
        "phoneNumberDetails.carrier",
        "phoneNumberDetails.countryCodeISO",
        "phoneNumberDetails.lineType",
        "phoneNumberDetails.updatedAt",
        "signupDate",
        "signupSource",
        "userId",
        "profileUpdatedAt",
    ],
) -> PandasDF:
    """user_history dataframe"""

    base_url = urls["export"]

    fields_to_query = create_only_fields(fields_list)

    url = f"{base_url}?dataTypeName=user&range=All&startDateTime={start_date}&endDateTime={end_date}&{fields_to_query}"

    data = get_export_data(url, get_headers())

    df = csv_to_dataframe(data)

    now = datetime.now()
    df["meta"] = str(
        {
            "start_date": start_date,
            "end_date": end_date,
            "url": url,
            "requested_on": now,
        }
    )
    return df
