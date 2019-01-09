"""Handle configuration files for Shecan CLI project."""

from collections import namedtuple

from pathlib import Path

DNSConfig = namedtuple('DNSConfig', ['db_path'])


def get_config():
    """Return DNSConfig object."""
    dns_db_path = Path('~/.dns_db.json').expanduser()
    return DNSConfig(str(dns_db_path))
