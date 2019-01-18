import argparse
import os

from exceptions import LrException

import network.terraform as tf
import network.config

EPILOG = """
Uses Terraform to destroy the network. The network is not stopped first. If
this behavior is desired, `lrmgr network stop` should be called first.
"""

def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('destroy', parents=[parent_parser])
    parser.epilog = EPILOG

    parser.add_argument('id', type=str, help='name of the network')


def do(args):
    network_config = network.config.load(args.id)

    tf.destroy(network_config)

    network.config.destroy_dir(args.id)
