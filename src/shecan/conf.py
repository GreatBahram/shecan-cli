"""Module containing classes to access the shecan configuration."""

from configparser import ConfigParser
from pathlib import Path


class ShecanConfig:
    """Wrapper class for Shecan configuraton."""

    def __init__(self, config_file: str) -> None:
        self.config_file = config_file
        self._parser = ConfigParser()
        self._name = "shecan"
        self._initialize()

    def _initialize(self):
        """Initialize the shecan config file"""
        if "shecan" not in self._parser:
            self._parser.add_section(self._name)

    def _read_config(self):
        """Read the configuration from a file."""
        self._parser.read(self.config_file)

    def __enter__(self):
        self._read_config()
        return self

    def __exit__(self, *exceptions):
        with open(self.config_file, mode="wt") as fp:
            self._parser.write(fp)

    def update(self, ips: list):
        """Store all Shecan's ip addresses."""
        self._parser[self._name]["dns-ips"] = ",".join(ips)

    def list_dns(self):
        """Return list of Shecan's dns servers."""
        return self._parser[self._name]["dns-ips"].split(",")

    def delete(self,) -> None:
        """Remove all Shecan's dns servers from configuration."""
        self._parser.remove_section(self._name)
        self._initialize()

    def remove(self,) -> None:
        """Remove the configuration file."""
        Path(self.config_file).unlink()
