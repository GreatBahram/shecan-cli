"""
Shecan CLI
~~~~~~~~~~~~~~~~~~~~~
The Shecan CLI https://shecan.ir
"""

from .api import current_dns, list_dns, update
from .utils import get_shecan_ips as get_ips

__all__ = [
    "current_dns",
    "get_ips",
    "list_dns",
    "update",
]

version = "0.3.0"
