"""
shecan.api
~~~~~~~~~~~~
This module implements Main API for shecan-cli project..
"""

from collections import namedtuple
from typing import List, NamedTuple

from shecan import dnsdb_tinydb
from shecan.utils import get_ips
from shecan.exceptions import UninitializedDatabase


# DNS element Types: [ip: str, id: int]
class DNS(NamedTuple):
    ip: str = None
    id: int = None


# Resolver element Types: [type: str, ip: str]
class Resolver(NamedTuple):
    type : str = None
    ip: str = None


def add(dns) -> int:
    """ Add a DNS (a DNS object) to the dns database."""
    if not isinstance(dns, DNS):
        raise TypeError('dns must be DNS object.')
    if _dnsdb is None:
        raise UninitializedDatabase()
    dns_id = _dnsdb.add(dns._asdict())
    return dns_id


def get(dns_id: int) -> DNS:
    """ Return a DNS object with matching dns_id."""
    if not isinstance(dns_id, int):
        raise TypeError('dns_id must be an int.')
    if _dnsdb is None:
        raise UninitializedDatabase()
    dns_dict = _dnsdb.get(dns_id)
    if dns_dict:
        return DNS(**dns_dict)
    raise KeyError('DNS ID does not exist.')


def delete_all() -> None:
    """ Remove all dns record from db."""
    if _dnsdb is None:
        raise UninitializedDatabase()
    _dnsdb.delete_all()


def list_dns() -> List[DNS]:
    """ Return a list of DNS objects."""
    if _dnsdb is None:
        raise UninitializedDatabase()
    return [DNS(**dns) for dns in _dnsdb.list_dns()]


def current_dns() -> List[Resolver]:
    """ List current dns servers in /etc/resolv.conf."""
    resolv_list = []
    with open('/etc/resolv.conf', mode='rt') as resovl_file:
        for line in resovl_file:
            if line.startswith('#'):
                continue
            resolv_list.append(Resolver(*line.split()[:2]))
    return resolv_list


def update() -> None:
    """ Retrieve a list of DNS name servers and store them into db."""
    ips = get_ips()
    delete_all()
    for ip in ips:
        uniq_id = unique_id()
        dns = DNS(ip, uniq_id)
        add(dns)

def unique_id() -> str:
    """ Return an integer that does not exist in the db."""
    if _dnsdb is None:
        raise UninitializedDatabase()
    return _dnsdb.unique_id()


_dnsdb = None


def start_dns_db(db_path: str) -> None:
    """ Connect API functions to a db."""
    if not isinstance(db_path, str):
        raise TypeError('db_path must be a string.')
    global _dnsdb
    _dnsdb = dnsdb_tinydb.start_dns_db(db_path)


def stop_dns_db() -> None:
    """ Disconnect API functions from db."""
    global _dnsdb
    _dnsdb.stop_dns_db()
    _dnsdb = None
