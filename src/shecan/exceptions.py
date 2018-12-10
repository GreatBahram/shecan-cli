"""
shecan.exceptions
~~~~~~~~~~~~~~~~~~~
This module contains the set of Shecan's exceptions.
"""


class DNSException(Exception):
    """ A DNS error has occured."""


class UninitializedDatabase(DNSException):
    """Call shecan.start_dns_db() before other functions."""
