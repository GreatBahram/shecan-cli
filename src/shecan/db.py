"""Module containing classes to access the shecan configuration."""

from configparser import ConfigParser
from pathlib import Path
from typing import Self

DB_PATH = Path("~/.dns_db.cfg").expanduser()


class ShecanConfig:
    """Wrapper class for Shecan configuraton."""

    def __init__(self, config_file: str = DB_PATH) -> None:
        self.config_file = config_file
        self._parser = ConfigParser()
        self._name = "shecan"

    def _initialize(self) -> None:
        """Initialize the shecan config file"""
        if not Path(self.config_file).exists():
            with open(self.config_file, mode="w") as fp:
                fp.write(f"[{self._name}]")

    def _read_config(self) -> None:
        """Read the configuration from a file."""
        self._initialize()
        self._parser.read(self.config_file)

    def __enter__(self) -> Self:
        self._read_config()
        return self

    def __exit__(self, *exceptions: object) -> None:
        with open(self.config_file, mode="w") as fp:
            self._parser.write(fp)

    def update(self, ips: list) -> None:
        """Store all Shecan's ip addresses."""
        self._parser[self._name]["dns-ips"] = ",".join(ips)

    def list_dns(self) -> list[str]:
        """Return list of Shecan's dns servers."""
        try:
            ips = self._parser[self._name]["dns-ips"].split(",")
        except KeyError:
            ips = []
        return ips

    def delete(
        self,
    ) -> None:
        """Remove all Shecan's dns servers from configuration."""
        self._parser.remove_section(self._name)
        self._initialize()

    def remove(
        self,
    ) -> None:
        """Remove the configuration file."""
        Path(self.config_file).unlink()
