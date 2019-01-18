import argparse
import os

from exceptions import LrException

import network.config
import network.terraform as tf


EPILOG = """
Print all the ips, in order of network index, for a given network.
"""


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('show', parents=[parent_parser])
    parser.epilog = EPILOG

    parser.add_argument('id', type=str, help='name of network to show')
    parser.add_argument('--delim', type=str, help='delimiter to print between ips', default=' ')
    parser.add_argument('--prefix', type=str, help='prefix to print before ip', default='')
    parser.add_argument('--suffix', type=str, help='suffix to print before ip', default='')


def do(args):
    try:
        config = network.config.load(args.id)
        ips = tf.get_network_ips(config)
        for ip in ips:
            print(args.prefix + ip + args.suffix + args.delim, end='')
        print()
    except KeyError:
        print('Network not found %s' % args.id)
