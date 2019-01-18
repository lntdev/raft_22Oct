import argparse
import os
import time
import yaml

from exceptions import LrException

import network.terraform as tf
import network.ansible as ansible
import network.config

EPILOG = """
Use Ansible to upgrade the version of sawtooth installed on the network.
"""


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('upgrade', parents=[parent_parser])
    parser.epilog = EPILOG

    parser.add_argument('id', type=str, help='name of network to be upgraded')
    parser.add_argument('--config', type=str, help='new configuration file for network')


def do(args):
    config = network.config.load(args.id)
    print(config)
    ansible.playbook("upgrade_sawtooth", config, retries=5, delay=60)
