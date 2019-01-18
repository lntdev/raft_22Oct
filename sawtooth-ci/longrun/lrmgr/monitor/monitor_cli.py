import argparse
import time

from exceptions import LrException

import network.config

import monitor.stats


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('monitor', parents=[parent_parser])
    parser.add_argument('id', type=str, help='name of network to monitor')
    parser.add_argument('tag', type=str, help='text to tag the stats with')
    parser.add_argument(
        '--period', type=int,
        help='seconds between stats posts',
        default='300'
    )
    parser.add_argument(
        '--url', type=str, help='endpoint to post to',
        default='http://localhost:20800/log'
    )


def do(args, on_invalid):
    config = network.config.load(args.id) 

    while True:
        message = {}
        message['stats'] = monitor.stats.get(config)
        message['tag'] = args.tag
        message['network'] = args.id
        monitor.stats.post(args.url, message)
        time.sleep(args.period)
