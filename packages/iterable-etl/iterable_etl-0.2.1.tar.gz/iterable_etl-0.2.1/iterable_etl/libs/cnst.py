"""constants"""

import os
from datetime import date
from typing import Any, Dict

urls = {
    "lists": "https://api.iterable.com/api/lists",
    "campaigns": "https://api.iterable.com/api/campaigns",
    "metrics": "https://api.iterable.com/api/campaigns/metrics",
    "lists_get_users": "https://api.iterable.com/api/lists/getUsers?listId=",
    "export": "https://api.iterable.com/api/export/data.csv",
}


def get_headers() -> Dict[str, Any]:
    """header config for Iterable API"""
    headers = {
        "Api-Key": os.environ.get("ITERABLE_KEY"),
        "Content-Type": "application/json",
    }
    return headers


def get_todays_date():
    """today"""
    today = date.today()
    return today.strftime("%Y-%m-%d")
