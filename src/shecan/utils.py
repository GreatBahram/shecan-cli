"""
shecan.utils
~~~~~~~~~~~~~~
This module provides utility functions that are used within shecan.
"""

from contextlib import contextmanager
from typing import Tuple

import requests
from bs4 import BeautifulSoup

import shecan

# Variables
BASE_URL = 'https://shecan.ir/'
CSS_SELECTOR = '.shecan-dns-ips'


def get_ips(url: str = BASE_URL, selector: str = CSS_SELECTOR) -> Tuple[str]:
    """ Retrieve shecan DNS IP addresses."""
    with requests.get(url) as req:
        data = req.text
    soup = BeautifulSoup(data, 'lxml')
    ips = soup.select(selector)
    ips = tuple(item.string for item in ips)
    return ips


@contextmanager
def _dns_db():
    config = shecan.config.get_config()
    shecan.start_dns_db(config.db_path)
    yield
    shecan.stop_dns_db()
