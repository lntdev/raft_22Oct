import argparse
import os
import time
import yaml

from exceptions import LrException

import network.terraform as tf
import network.ansible as ansible
import network.config
import network.update

EPILOG = """
Uses Terraform to create a new network and Ansible to deploy Hyperledger
Sawtooth to the network. The network id given must be unique and is used to
refer to the network in other commands. Configuration can be done using a
config file. If no config is passed, uses a set of defaults that are useful for
testing the tool. The default config is included as an example in
`lrmgr/network/data/`.
"""

def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('create', parents=[parent_parser])
    parser.epilog = EPILOG

    parser.add_argument('id', type=str, help='name of network to be created')
    parser.add_argument('--config', type=str, help='network configuration file', required=True)


def do(args):
    # 1. Create dir to store network info
    network.config.create_dir(args.id)

    # 2. Save network info for future reference
    network.config.save(args)
    config = network.config.load(args.id)

    # 3. Create the network in terraform
    tf.create(config)

    # 4. Install sawtooth and configure
    time.sleep(3)
    ansible.playbook("setup_sawtooth", config, retries=5, delay=60)
