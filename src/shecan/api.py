"""
shecan.api
~~~~~~~~~~~~
This module implements Main API for shecan-cli project..
"""

from typing import List, NamedTuple

from shecan.conf import ShecanConfig
from shecan.utils import get_shecan_ips
from shecan.exceptions import UninitializedDatabase


# DNS element Types: [ip: str, id: int]
class DNS(NamedTuple):
    ip: str = None
    id: int = None


# Resolver element Types: [type: str, ip: str]
class Resolver(NamedTuple):
    type: str = None
    ip: str = None


def add(dns) -> int:
    """ Add a DNS (a DNS object) to the dns database."""
    if not isinstance(dns, DNS):
        raise TypeError("dns must be DNS object.")
    with ShecanConfig() as config:
        config.add(dns._asdict())


_dnsdb = None


def get(dns_id: int) -> DNS:
    """ Return a DNS object with matching dns_id."""
    if not isinstance(dns_id, int):
        raise TypeError("dns_id must be an int.")
    if _dnsdb is None:
        raise UninitializedDatabase()
    dns_dict = _dnsdb.get(dns_id)
    if dns_dict:
        return DNS(**dns_dict)
    raise KeyError("DNS ID does not exist.")


def delete_all() -> None:
    """Remove all the DNS records from the configuration file."""
    conf = ShecanConfig()
    conf.delete()


def list_dns() -> List[DNS]:
    """Return a list of DNS objects."""
    if _dnsdb is None:
        raise UninitializedDatabase()
    return [DNS(**dns) for dns in _dnsdb.list_dns()]


def current_dns() -> List[Resolver]:
    """ List current dns servers in /etc/resolv.conf."""
    resolv_list = []
    with open("/etc/resolv.conf", mode="rt") as resovl_file:
        for line in resovl_file:
            if line.startswith("#"):
                continue
            resolv_list.append(Resolver(*line.split()[:2]))
    return resolv_list


def update() -> None:
    """ Retrieve a list of DNS name servers and store them into db."""
    ips = get_ips()
    delete_all()
    for index, ip in enumerate(ips, start=1):
        uniq_id = unique_id()
        dns = DNS(ip, f"dns_{index}")
        add(dns)
