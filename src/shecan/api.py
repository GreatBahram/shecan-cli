"""
shecan.api
~~~~~~~~~~~~
This module implements Main API for shecan-cli project..
"""

import sys
from typing import List, NamedTuple

from shecan.db import ShecanConfig
from shecan.utils import get_shecan_ips


# Resolver element Types: [type: str, ip: str]
class Resolver(NamedTuple):
    type: str = None
    ip: str = None


def add(ips) -> int:
    """Add a DNS (a DNS object) to the dns database."""
    with ShecanConfig() as config:
        config.update(ips)


def reset() -> None:
    """Remove all the DNS records from the configuration file."""
    conf = ShecanConfig()
    conf.delete()


def list_dns():
    """Return a list of DNS objects."""
    with ShecanConfig() as conf:
        ips = conf.list_dns()
    return ips


def current_dns() -> List[Resolver]:
    """ List current dns servers in /etc/resolv.conf."""
    resolv_list = []
    if sys.platform == "linux":
        with open("/etc/resolv.conf", mode="rt") as resovl_file:
            for line in resovl_file:
                if line.startswith("#"):
                    continue
                resolv_list.append(Resolver(*line.split()[:2]))
    return resolv_list


def update() -> None:
    """Retrieve a list of DNS name servers and store them into db."""
    ips = get_shecan_ips()
    if ips:
        reset()
        add(ips)
