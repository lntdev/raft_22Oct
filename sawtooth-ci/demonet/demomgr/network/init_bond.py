import argparse
import os

from exceptions import LrException

import network.terraform as tf
import network.config
import runner

BIN_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))),
    'bin'
)


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('init_bond', parents=[parent_parser])

    parser.add_argument('id', type=str, help='name of network to connect to')
    parser.add_argument('node', type=int, help='node to connect to')


def do(args):
    # ip = ansible.get_node_ip(args.node, args.id) 
    config = network.config.load(args.id)
    ip = tf.get_node_ip(args.node, config)

    cwd = os.getcwd() # Need this to use ansible.cfg
    os.chdir(BIN_PATH)

    runner.run([
        os.path.join(BIN_PATH, "init_bond"), config['sawtooth_path'], ip
    ])
    os.chdir(cwd)
