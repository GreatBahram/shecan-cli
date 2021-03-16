"""
shecan.utils
~~~~~~~~~~~~~~
This module provides utility functions that are used within shecan.
"""
from typing import Tuple
from urllib import request

from bs4 import BeautifulSoup

BASE_URL = "https://shecan.ir/"
CSS_SELECTOR = ".shecan-dns-ips"


def get_shecan_ips(url: str = BASE_URL, selector: str = CSS_SELECTOR) -> Tuple[str]:
    """ Retrieve shecan DNS IP addresses."""
    data = request.urlopen(BASE_URL).read().decode("utf-8")
    soup = BeautifulSoup(data, "lxml")
    ips = soup.select(selector)
    return tuple(item.string for item in ips)
