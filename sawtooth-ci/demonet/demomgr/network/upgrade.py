import argparse
import os
import time
import yaml

from exceptions import LrException

import network.terraform as tf
import network.ansible as ansible
import network.config


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('upgrade', parents=[parent_parser])

    parser.add_argument('id', type=str, help='name of network to be created')


def do(args):

    config = network.config.load(args.id)

    genesis_hostname = tf.get_node_name(0, config)
    ansible.playbook("upgrade_sawtooth", config, [
        "sawtooth_packages='{}'".format(
            config['sawtooth_packages']),
    ], retries=5, delay=60)
