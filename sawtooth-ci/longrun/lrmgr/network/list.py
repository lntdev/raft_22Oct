import argparse
import os

from exceptions import LrException

import network.config
import network.terraform as tf


EPILOG = """
List all networks and nodes of which the tool is aware. `lrmgr network connect`
should be used to SSH into the nodes.
"""


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('list', parents=[parent_parser])
    parser.epilog = EPILOG


def do(args):
    networks = network.config.list_networks()
    for nid in networks:
        config = network.config.load(nid)
        ips = tf.get_network_ips(config)
        format_str = '{:<8} {:<3} ' + '{:<16}'
        print(format_str.format(nid, 'ID', 'IP'))
        for idx, ip in enumerate(ips):
            print(format_str.format('', idx, ip))
        print()
