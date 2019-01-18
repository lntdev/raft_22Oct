import argparse
import os

from exceptions import LrException

import network.ansible as ansible
import network.config


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('stop', parents=[parent_parser])

    parser.add_argument('id', type=str, help='name of network to start')


def do(args):
    config = network.config.load(args.id)

    ansible.playbook("stop_sawtooth", config)
