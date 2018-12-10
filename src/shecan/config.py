"""Handle configuration files for Shecan CLI project."""

from collections import namedtuple

import os

DNSConfig = namedtuple('DNSConfig', ['db_path'])


def get_config():
    """Return DNSConfig object after reading config file."""
    config_file = os.path.expanduser('~/.dns.config')
    dns_db_path = os.path.expanduser('~/.dns_db.json')
    return DNSConfig(dns_db_path)
