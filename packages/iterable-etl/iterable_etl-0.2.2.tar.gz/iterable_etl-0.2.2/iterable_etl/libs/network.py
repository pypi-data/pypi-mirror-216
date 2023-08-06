"""network"""

from typing import Any, Dict
from urllib.parse import urlparse, urlunparse

import requests
from requests import Response

from iterable_etl.libs.dbg import dbg


def trim_string(string: str):
    if len(string) > 150:
        trimmed_string = string[:150].strip() + "..."
        return trimmed_string
    else:
        return string


def get_data(api_url: str, headers: Dict[str, str]) -> Response:
    """Make a GET request to the Iterable API and return the data."""
    dbg_url = trim_string(api_url)
    dbg("Making request to {api_url}", api_url=dbg_url)
    response = requests.get(api_url, headers=headers, timeout=120)
    dbg("{api_url} response code {code}", api_url=dbg_url, code=response.status_code)
    response.raise_for_status()
    return response


def get_data_json(api_url: str, headers: Dict[str, str]) -> Dict[str, Any]:
    data = get_data(api_url, headers)
    return data.json()


def get_data_text(api_url: str, headers: Dict[str, str]) -> str:
    data = get_data(api_url, headers)
    return data.text


def get_data_csv(api_url: str, headers: Dict[str, str]) -> str:
    data = get_data(api_url, headers)
    content = data.content.decode("utf-8")
    return content
