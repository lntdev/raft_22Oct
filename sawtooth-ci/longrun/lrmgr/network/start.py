import argparse
import os

from exceptions import LrException

import network.ansible as ansible
import network.config

EPILOG = """
Start the network with the given id. Must already be created. The services that
are actually started by this command are configured when the network is created
in the config file that is passed.
"""


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('start', parents=[parent_parser])
    parser.epilog = EPILOG

    parser.add_argument('id', type=str, help='name of network to start')


def do(args):
    config = network.config.load(args.id)
    ansible.playbook("start_sawtooth", config)
