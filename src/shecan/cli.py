import argparse
import logging
import shutil
import socket
import sys
from os import path
from tempfile import gettempdir

import shecan.log
from shecan import config
from shecan.utils import _dns_db

logger = logging.getLogger(__name__)


def list_dns():
    """ List dns servers in db."""
    formatstr = "{: >4} {: >10}"
    print(formatstr.format('ID', 'IP'))
    print(formatstr.format('--', '-----'))
    with _dns_db():
        for dns in shecan.list_dns():
            print(formatstr.format(dns.id, dns.ip))


def update_dns_servers():
    """ Get list of Shecan dns name servers and store them into database."""
    with _dns_db():
        shecan.update()

def verify_dns():
    result = socket.gethostbyname('check.shecan.ir')
    with _dns_db():
        if result in [dns.ip for dns in shecan.list_dns()]:
            print('Verified ✓')
        else:
            print('Unverified X')

def shecan_cli():
    parser = argparse.ArgumentParser(description="CLI for shecan.ir website.")
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Turn on extra logging (DEBUG level)",
    )
    subparsers = parser.add_subparsers()

    # `list` command
    get = subparsers.add_parser(
        "list",
        help="List Shecan's DNS servers.",
    )
    get.set_defaults(op="list")

    # `verify` command
    verify = subparsers.add_parser(
        "verify", help="check DNS validity."
    )
    verify.set_defaults(op="verify")

    # `set` command
    set_ = subparsers.add_parser(
        "set", help="Set DNS configuration."
    )
    set_.add_argument(
        "--id",
        action="store",
        type=int,
        default=False,
        help="Which dns server should be set.",
    )
    group = set_.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--temporary",
        action="store_const",
        const='temporary',
        dest='mode',
        help="Write the DNS record inside /etc/resolv.conf file.",
    )
    group.add_argument(
        "--permanent",
        action="store_const",
        const='permanent',
        dest='mode',
        default=False,
        help="Write the DNS record permanently file.",
    )
    set_.set_defaults(op="set")

    # `restore` command
    restore = subparsers.add_parser(
        "restore", help="Restore old DNS configuration."
    )
    restore.set_defaults(op='restore')

    # `update` command
    update = subparsers.add_parser(
        "update",
        help="Update the database.",
    )
    update.set_defaults(op="update")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        return 1

    shecan.log.setup_logging(args)

    if args.op == 'list':
        list_dns()
    elif args.op == 'update':
        update_dns_servers()
    elif args.op == 'verify':
        verify_dns()
    elif args.op == 'set':
        with _dns_db():
            if args.id:
                dns = [shecan.get(args.id)]
            else:
                dns = shecan.list_dns()
            if args.mode == 'temporary':
                resolv_file = path.join('/etc', 'resolv.conf')
                tmp_resolv_file = path.join(gettempdir(), 'resolv.conf')
                if path.exists(resolv_file):
                    try:
                        shutil.move(resolv_file, tmp_resolv_file)
                        logger.debug(f'shecan moved {resolv_file} to {tmp_resolv_file}')
                        with open(resolv_file, mode='wt') as r_file:
                            for item in dns:
                                r_file.write(f'nameserver {item.ip}\n')
                    except OSError as e:
                        logger.error(
                            f'Could not move resolv file ({resolv_file}) to '
                            + f' {tmp_resolv_file}: {e}')
                else:
                    logger.info(f"No resolv file to move ({resolv_file})")
            else:
                raise NotImplementedError('This feature has not been implemented yet.')
    elif args.op == 'restore':
        tmp_resolv_file = path.join(gettempdir(), 'resolv.conf')
        resolv_file = path.join('/etc', 'resolv.conf')
        if path.exists(tmp_resolv_file):
            try:
                shutil.move(tmp_resolv_file, resolv_file)
                logger.debug(f'shecan moved {tmp_resolv_file} to {resolv_file}')
            except OSError as e:
                logger.error(
                    f'Could not move temporary resolv file ({tmp_resolv_file}) to '
                    + f'({resolv_file}): {e}')
        else:
            logger.info(f"Temporary file not found ({tmp_resolv_file}).")



if __name__ == '__main__':
    shecan_cli()
