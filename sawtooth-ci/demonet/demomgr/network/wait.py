import argparse
import yaml
import os
import time
import urllib.request
from urllib.error import URLError

from exceptions import LrException

import network.terraform as tf
import network.config

def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('wait', parents=[parent_parser])

    parser.add_argument( 'id', type=str, help='name of network to connect to')


def do(args):
    # ip = ansible.get_node_ip(args.node, args.id) 
    config = network.config.load(args.id)
    ips = tf.get_network_ips(config)

    count = 0
    endpoints = []
    while True:
        print("Still waiting on %s" % args.id)
        try:
            url = "http://{}:8800/store/EndpointRegistryTransaction/*?p=1".format(ips[0])
            request = urllib.request.Request(url)
            result = urllib.request.urlopen(request).read().decode()
            data = yaml.load(result)
        except:
            print("Couldn't reach node 0")
            data = {}

        count = len(data.keys())
        for key in data:
            host = data[key]['Host']
            if host not in endpoints:
                endpoints.append(host)
                print("Found endpoint: %s (%d/%d)" % (
                    data[key]['Host'], len(endpoints), len(ips)))

        if count != len(ips):
            time.sleep(3)
        else:
            break
