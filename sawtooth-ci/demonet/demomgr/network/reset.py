import argparse
import os

from exceptions import LrException

import network.ansible as ansible
import network.config


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('reset', parents=[parent_parser])

    parser.add_argument('id', type=str, help='name of network to start')


def do(args):
    config = network.config.load(args.id)

    playbook = ansible.playbook("reset_sawtooth", config)
