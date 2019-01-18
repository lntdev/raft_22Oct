import argparse

import network.create
import network.destroy
import network.connect
import network.start
import network.stop
import network.reset
import network.upgrade
import network.init_bond
import network.wait

CMDS = {
    'create': network.create,
    'destroy': network.destroy,
    'connect': network.connect,
    'start': network.start,
    'stop': network.stop,
    'reset': network.reset,
    'upgrade': network.upgrade,
    'init_bond': network.init_bond,
    'wait': network.wait,
}

def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('network', parents=[parent_parser])

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
