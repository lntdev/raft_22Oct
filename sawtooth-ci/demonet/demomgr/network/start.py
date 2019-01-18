import argparse
import os

from exceptions import LrException

import network.ansible as ansible
import network.config


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('start', parents=[parent_parser])

    parser.add_argument('id', type=str, help='name of network to start')


def do(args):
    config = network.config.load(args.id)

    ansible.playbook("start_sawtooth", config, [
        "genesis_tag='{}'".format(
            ansible.get_name_tag(0, config['network_id'])
        ),
        "sawtooth_validator_ledger_type='{}'".format(
            config['sawtooth_ledger_type']),
    ])

