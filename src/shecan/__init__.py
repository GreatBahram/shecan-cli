"""
Shecan CLI
~~~~~~~~~~~~~~~~~~~~~
The Shecan CLI https://shecan.ir
"""

from .api import current_dns, get, list_dns, start_dns_db, stop_dns_db, update
from . import config

__all__ = [
    "current_dns",
    "get",
    "list_dns",
    "start_dns_db",
    "stop_dns_db",
    "update",
    "config",
]

version = "0.2.4"
