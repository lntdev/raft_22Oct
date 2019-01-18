import argparse

import network.connect
import network.create
import network.destroy
import network.list
import network.show
import network.reset
import network.start
import network.stop
import network.wait
import network.update
import network.upgrade
import network.install_pr

CMDS = {
    'connect': network.connect,
    'create': network.create,
    'destroy': network.destroy,
    'list': network.list,
    'show': network.show,
    'reset': network.reset,
    'start': network.start,
    'stop': network.stop,
    'wait': network.wait,
    'update': network.update,
    'upgrade': network.upgrade,
    'install_pr': network.install_pr,
}

EPILOG = """
The network subcommand handles all network management tasks including. See the
subcommand usage for more details. All commands should be idempotent unless
noted otherwise.
"""

def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('network', parents=[parent_parser])
    parser.epilog = EPILOG

    network_subparser = parser.add_subparsers(
        title='subcommands', dest='network_command'
    )

    for cmd in CMDS:
        CMDS[cmd].add_parser(network_subparser, parent_parser)


def do(args, on_invalid):
    if args.network_command in CMDS:
        CMDS[args.network_command].do(args)
    else:
        on_invalid()
