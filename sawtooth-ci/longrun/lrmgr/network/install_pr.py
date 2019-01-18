import argparse
import os
import time
import yaml

from exceptions import LrException

import network.terraform as tf
import network.ansible as ansible
import network.config

EPILOG = """
Use Ansible to install debs from a jenkins PR.
"""


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('install_pr', parents=[parent_parser])
    parser.epilog = EPILOG

    parser.add_argument('pr', type=str, help='number of pr to install.')
    parser.add_argument('id', type=str, help='name of network to install to.')


def do(args):
    config = network.config.load(args.id)
    print(config)
    ansible.playbook("install_pr", config, playbook_args=["pr_number='{}'".format(args.pr)], retries=5, delay=60)
