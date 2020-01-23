"""
shecan.utils
~~~~~~~~~~~~~~
This module provides utility functions that are used within shecan.
"""
from typing import Tuple

import requests

from bs4 import BeautifulSoup

BASE_URL = "https://shecan.ir/"
CSS_SELECTOR = ".shecan-dns-ips"


def get_shecan_ips(url: str = BASE_URL, selector: str = CSS_SELECTOR) -> Tuple[str]:
    """ Retrieve shecan DNS IP addresses."""
    with requests.get(url) as req:
        data = req.text
    soup = BeautifulSoup(data, "lxml")
    ips = soup.select(selector)
    return tuple(item.string for item in ips)
