"""
Shecan CLI
~~~~~~~~~~~~~~~~~~~~~
The Shecan CLI https://shecan.ir
"""

from .api import current_dns, get, list_dns, ShecanConfig, update
from . import config

__all__ = [
    "current_dns",
    "get",
    "list_dns",
    "update",
    "config",
]

version = "0.2.4"
