import argparse
import os
import time

from exceptions import LrException

import network.terraform as tf
import network.config

import sim.config
import sim.timeline


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('run', parents=[parent_parser])

    parser.add_argument('timeline', type=str,
        help='path to simulation timeline')

    parser.add_argument('network_id', type=str, 
        help='name of network to run sim against')


def do(args):

    network_config = network.config.load(args.network_id)
    timeline = sim.timeline.load(args.timeline)
    # timeline = sim.config.load(args.timeline)
    print(timeline)

    sim.timeline.run(timeline, network_config)
