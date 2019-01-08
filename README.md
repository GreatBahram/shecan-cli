# Shecan CLI

[![image](https://img.shields.io/pypi/v/shecan.svg)](https://pypi.org/project/shecan/)
[![image](https://img.shields.io/pypi/l/shecan.svg)](https://pypi.org/project/shecan/)
[![image](https://img.shields.io/pypi/pyversions/shecan.svg)](https://pypi.org/project/shecan/)
[![image](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/GreatBahram)

------------------------------------------------------------------------

The Shecan CLI is used to configure your DNS name server based on Shecan website from the command line.

For more about Shecan see https://shecan.ir/

## Installation

The following instructions will place the shecan executable in a
virtualenv under `shecan/bin/shecan`.

- Shecan **requires** `>= Python 3.6.1`

### pip

This installs the latest stable, released version.

```
$ python3.6 -m venv shecan
$ shecan/bin/pip install shecan
```
# Quickstart

* Run ``shecan update`` - It will get shecan DNS name servers and save them into database.
* Run ``shecan list`` It will show shecan DNS name servers from the database.
* Run ``shecan set --temporary`` It will configure your DNS temporarily by moving your current `/etc/resolv.conf` file and replace it with shecan DNS name server. **If you permission problem** run the command this way: `sudo $(which shecan) set --temporary`.
* Run ``shecan verify`` It will check your DNS configuration and make sure that shecan works fine for you.
* Run ``shecan restore`` It will restore your previous DNS configuration.
* Run ``shecan show`` It will print your current DNS configuration.
* Run ``shecan --version`` It will show shecan's version.
* Run ``shecan --help`` It will show full command-line options and subcommands.
