import argparse
import os
import time
import yaml

from exceptions import LrException

import network.terraform as tf
import network.ansible as ansible
import network.config

EPILOG = """
Use Ansible to apply the new config file to the network. This only updates
configuration of the network. If the topology needs to change (i.e., Terraform
needs to be used) then `lrmgr network create` should be used instead.
"""


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('update', parents=[parent_parser])
    parser.epilog = EPILOG

    parser.add_argument('id', type=str, help='name of network to be updated')
    parser.add_argument('--config', type=str, help='new configuration file for network')


def do(args):
    config = network.config.load(args.id)
    ansible.playbook("setup_sawtooth", config, retries=5, delay=60)
