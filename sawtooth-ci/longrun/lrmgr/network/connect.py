import argparse
import os

from exceptions import LrException

import network.terraform as tf
import network.config

EPILOG = """
Use SSH to connect to the given node on the given network. Nodes are 0-indexed
as shown in `lrmgr network list`.
"""

def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('connect', parents=[parent_parser])

    parser.add_argument( 'id', type=str, help='name of network to connect to')
    parser.add_argument( 'node', type=int, help='node to connect to')


def do(args):
    # ip = ansible.get_node_ip(args.node, args.id) 
    config = network.config.load(args.id)
    ip = tf.get_node_ip(args.node, config)
    os.execlp(
        "ssh", "ssh", 
        "ubuntu@{}".format(ip), 
        "-i", config['key_file']
    )
