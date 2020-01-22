""" Module containing classes to access the shecan configuration."""

from configparser import ConfigParser


class ShecanConfig:
    """Wrapper class Shecan configuraton."""

    def __init__(self, config_file: str) -> None:
        self.config_file = config_file

    def initialize(self):
        """Initialize the shecan config file"""
        pass

    def read_config(self):
        """ Read the configuration from a file."""
        self.config = ConfigParser()
        self.config.read(self.config_file)

    def add(self, dns: dict):
        pass

    def list_dns(self):
        """"""
        pass

    def update(self):
        pass

    def delete(self,) -> None:
        """Remove all shecan's dns servers from configuratio."""
        pass

    def remove(self,) -> None:
        """Remove the configuration file."""
        pass
