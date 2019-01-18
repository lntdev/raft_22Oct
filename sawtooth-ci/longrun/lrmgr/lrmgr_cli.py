import argparse
import os
import traceback
import sys

from network import network_cli
from sim import sim_cli
from monitor import monitor_cli
from exceptions import LrException 

CMDS = {
    'network': network_cli,
    'sim': sim_cli,
}

EPILOG = """
The lrmgr tool handles the creation, maintenance, and destruction of
Hyperledger Sawtooth long running test networks. It also provides a general
purpose, modular, declarative simulation language for running test simulations
against a network.
"""

def create_parent_parser(prog_name):
    parent_parser = argparse.ArgumentParser(prog=prog_name, add_help=False)
    parent_parser.add_argument(
        '-v', '--verbose',
        action='count',
        help='enable more verbose output')

    return parent_parser


def create_parser(prog_name):
    parent_parser = create_parent_parser(prog_name)

    parser = argparse.ArgumentParser(
        parents=[parent_parser],
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(title='subcommands', dest='command')

    for cmd in CMDS:
        CMDS[cmd].add_parser(subparsers, parent_parser)

    return parser


def main(prog_name=os.path.basename(sys.argv[0]), args=sys.argv[1:]):
    parser = create_parser(prog_name)
    parser.epilog = EPILOG
    args = parser.parse_args(args)

    if args.verbose is None:
        verbose_level = 0
    else:
        verbose_level = args.verbose


    if args.command in CMDS:
        CMDS[args.command].do(args, parser.print_help)
    else:
        parser.print_help()


def _check_environment():
    for evar in ('AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY'):
        try:
            os.environ[evar]
        except KeyError:
            raise LrException(
                "Required environment variable `{}` not set.".format(evar))


def main_wrapper():
    try:
        _check_environment()
        main()
    except LrException as err:
        print("Error: {}".format(err), file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        pass
    except SystemExit as err:
        raise err
    except BaseException as err:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
