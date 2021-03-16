import argparse
import logging
import shutil
import socket
import sys
from pathlib import Path
from tempfile import gettempdir

from tabulate import tabulate

import shecan
import shecan.log

logger = logging.getLogger(__name__)


class TextStyle:
    GREEN = "\033[92m"
    RED = "\033[91m"
    NC = "\033[0m"  # No Color


def colorify(text: str, style: TextStyle):
    return f"{style}{text}{TextStyle.NC}"


def list_dns() -> None:
    """List dns servers in db."""
    dns_servers = shecan.list_dns()
    if not dns_servers:
        logger.debug("No DNS nameservers found! Update the shecan, please.")
    dns_servers = [(index, dns_ip) for index, dns_ip in enumerate(dns_servers, start=1)]
    print(tabulate(dns_servers, headers=["ID", "IP"], stralign="center"))


def update_resolv_file(content):
    resolv_file = Path("/etc", "resolv.conf")
    tmp_resolv_file = Path(gettempdir()).joinpath("resolv.conf")

    # copy current resolv file into temp dir
    try:
        shutil.copy(resolv_file, tmp_resolv_file)
    except FileNotFoundError:
        logger.warn(f"Resolv file not found ({resolv_file!s}).")
    except OSError as e:
        logger.error(
            f"Could not move resolv file ({resolv_file!s}) to "
            + f" {tmp_resolv_file!s}: {e}"
        )
    else:
        logger.debug(f"Shecan copied {resolv_file!s} to {tmp_resolv_file!s}")

    # update resolv file according to given content
    try:
        with open(resolv_file, mode="wt") as r_file:
            for line in content:
                r_file.write(line + "\n")
    except OSError as e:
        logger.error(f"Could not update resolv file: {e}")


def restore_resolv_file():
    tmp_resolv_file = Path(gettempdir(), "resolv.conf")
    resolv_file = Path("/etc", "resolv.conf")
    if tmp_resolv_file.exists():
        try:
            shutil.move(tmp_resolv_file, resolv_file)
            logger.debug(f"shecan moved {tmp_resolv_file} to {resolv_file}")
        except OSError as e:
            logger.error(
                f"Could not move temporary resolv file ({tmp_resolv_file}) to "
                + f"({resolv_file}): {e}"
            )
    else:
        logger.info(f"Temporary file not found ('{tmp_resolv_file}').")


def verify_dns() -> None:
    result = socket.gethostbyname("check.shecan.ir")
    shecan_dns_nameservers = shecan.list_dns()
    if result in shecan_dns_nameservers:
        print(f"Verified {colorify('✓', TextStyle.GREEN)}")
    else:
        print(f"Verified {colorify('X', TextStyle.RED)}")


def show_current_dns() -> None:
    """ List current dns servers in /etc/resolv.conf."""
    try:
        resolvers = shecan.current_dns()
    except FileNotFoundError:
        logger.error("Resolv file does not exist.")
        resolvers = []
    print(tabulate(resolvers, headers=["Type", "IP"], stralign="center"))


def shecan_cli():
    parser = argparse.ArgumentParser(description="CLI for shecan.ir website.")
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Turn on extra logging (DEBUG level)",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {shecan.version}"
    )
    subparsers = parser.add_subparsers()

    # `list` command
    get = subparsers.add_parser("list", help="List Shecan's DNS servers.")
    get.set_defaults(op="list")

    # `verify` command
    verify = subparsers.add_parser("verify", help="check DNS validity.")
    verify.set_defaults(op="verify")

    # `set` command
    set_ = subparsers.add_parser("set", help="Set DNS configuration.")
    set_.set_defaults(op="set")

    # `restore` command
    restore = subparsers.add_parser("restore", help="Restore old DNS configuration.")
    restore.set_defaults(op="restore")

    # `update` command
    update = subparsers.add_parser("update", help="Update the database.")
    update.set_defaults(op="update")

    # `show` command
    show = subparsers.add_parser(
        "show", help="Show your current dns servers in '/etc/resolv.conf'."
    )
    show.set_defaults(op="show")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return 1

    shecan.log.setup_logging(args)

    if args.op == "list":
        list_dns()
    elif args.op == "update":
        shecan.update()
    elif args.op == "verify":
        verify_dns()
    elif args.op == "set":

        if sys.platform != "linux":
            logger.error("Currently only Linux operating system is supported.")
            sys.exit(2)

        content = [f"nameserver {dns_ip}" for dns_ip in shecan.list_dns()]
        if not content:
            logger.error("Couldn't find Shecan DNS IP addresses in the config file.")
            sys.exit(1)

        update_resolv_file(content)

    elif args.op == "restore":
        restore_resolv_file()
    elif args.op == "show":
        show_current_dns()


if __name__ == "__main__":
    shecan_cli()
