import sys
from typing import NamedTuple

from shecan.db import ShecanConfig
from shecan.utils import get_shecan_ips


# Resolver element Types: [type: str, ip: str]
class Resolver(NamedTuple):
    type: str = None
    ip: str = None


def add(ips: tuple[str]) -> None:
    """Add a DNS (a DNS object) to the dns database."""
    with ShecanConfig() as config:
        config.update(ips)


def reset() -> None:
    """Remove all the DNS records from the configuration file."""
    conf = ShecanConfig()
    conf.delete()


def list_dns() -> list[str]:
    """Return a list of DNS objects."""
    with ShecanConfig() as conf:
        ips = conf.list_dns()
    return ips


def current_dns() -> list[Resolver]:
    """List current dns servers in /etc/resolv.conf."""
    resolv_list = []
    if sys.platform == "linux":
        with open("/etc/resolv.conf") as resovl_file:
            for line in resovl_file:
                line = line.strip()  # noqa: PLW2901
                if not line or line.startswith("#"):
                    continue
                resolv_list.append(Resolver(*line.split()[:2]))
    return resolv_list


def update() -> None:
    """Retrieve a list of DNS name servers and store them into db."""
    ips = get_shecan_ips()
    if ips:
        reset()
        add(ips)
