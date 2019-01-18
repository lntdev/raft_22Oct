import argparse
import os
import time
import yaml

from exceptions import LrException

import network.terraform as tf
import network.ansible as ansible
import network.config


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('create', parents=[parent_parser])

    parser.add_argument('id', type=str, help='name of network to be created')
    parser.add_argument('--config', type=str, help='network configuration file')


def do(args):
    # if args.id == "":
        # args.id = network.config.get_random_name()

    # 1. Create dir to store network info
    network.config.create_dir(args.id)

    # 2. Save network info for future reference
    network.config.save(args)
    config = network.config.load(args.id)

    # 3. Create the network in terraform
    tf.create(config)

    # 4. Install sawtooth and configure
    genesis_hostname = tf.get_node_name(0, config)
    ansible.playbook("setup_sawtooth", config, [
        "sawtooth_packages='{}'".format(
            config['sawtooth_packages']),

        "sawtooth_validator_transaction_families='{}'".format(
            ",".join(config['sawtooth_transaction_families'])),

        "genesis_node='{}'".format(genesis_hostname),

        "sawtooth_validator_ledger_type='{}'".format(config['sawtooth_ledger_type']),
        "sawtooth_local_validation='{}'".format(config['sawtooth_local_validation']),
        "sawtooth_logging_syslog_ip='{}'".format(config['sawtooth_syslog_ip']),
        "sawtooth_logging_syslog_facility='{}'".format(config['sawtooth_syslog_facility']),
    ], retries=5, delay=60)
