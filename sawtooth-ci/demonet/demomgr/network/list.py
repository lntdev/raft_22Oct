import argparse
import os

from exceptions import LrException

import network.terraform as tf
import network.ansible as ansible
import network.config


def add_parser(subparsers, parent_parser):
    parser = subparsers.add_parser('list', parents=[parent_parser])


def do(args):
    print("This command has not been implemented.")
