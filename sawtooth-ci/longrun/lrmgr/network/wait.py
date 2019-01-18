import argparse
import yaml
import os
import time
import requests

from exceptions import LrException

import network.terraform as tf
import network.config

EPILOG = """
Wait for all nodes of the network to be on the same block. This is useful for
waiting to start a simulation until after the network has settled down and is
in consensus.
"""


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('wait', parents=[parent_parser])
    parser.epilog = EPILOG

    parser.add_argument( 'id', type=str, help='name of network to connect to')


def do(args):
    # ip = ansible.get_node_ip(args.node, args.id) 
    config = network.config.load(args.id)
    ips = tf.get_network_ips(config)

    while True:
        heads = []
        for ip in ips:
            try:
                url = "http://{}:8080/blocks?count=1".format(ip)
                head = requests.get(url, timeout=0.1).json()["head"]
                print("[{}] has {}".format(ip, head[:6]))
                heads.append(head)

            except:
                print("Couldn't reach node {}".format(ip))
                heads = []
                break

        if len(set(heads)) == 1:
            print("All nodes on {}".format(heads[0][:6]))
            break
        else:
            print("Still waiting...")
            time.sleep(3)
