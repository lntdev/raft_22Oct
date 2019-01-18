import argparse
import os

from exceptions import LrException

import network.ansible as ansible
import network.config


EPILOG = """
Reset the data files on the network so it does not know about previous runs.
This does not affect the log files. This command deletes and recreates the data
directory, so it does not appear idempotent if run multiple times, but
practically speaking it is.
"""


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('reset', parents=[parent_parser])
    parser.epilog = EPILOG

    parser.add_argument('id', type=str, help='name of network to start')


def do(args):
    config = network.config.load(args.id)

    playbook = ansible.playbook("reset_sawtooth", config)
