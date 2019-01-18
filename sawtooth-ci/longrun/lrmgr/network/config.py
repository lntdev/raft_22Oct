import os
import getpass
import random
import shutil

import yaml

from exceptions import LrException

HOME_DIR = os.path.expanduser("~")
NETWORK_DIR = os.path.join(HOME_DIR, ".lrmgr", "network")
DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')

def create_dir(network_id):
    network_dir = get_dir(network_id)
    try:
        if not os.path.exists(network_dir):
            os.makedirs(network_dir)
    except OSError:
        raise LrException("Failed to create directory: {}".format(network_id))


def get_dir(network_id):
    return "{}/{}".format(NETWORK_DIR, network_id)


def list_networks():
    return os.listdir(NETWORK_DIR)

# def list_networks():


def get_random_name():
    try:
        with open(os.path.join(DATA_DIR, "names")) as fd:
            return random.choice(fd.read().split("\n"))
    except OSError:
        raise LrException("Failed to generate random name")


def destroy_dir(network_id):
    network_dir = get_dir(network_id)
    try:
        shutil.rmtree(network_dir)
    except OSError:
        raise LrException("Failed to remove directory and its contents: {}".format(
            network_dir))
 

def save(args):
    # Load config
    if args.config is not None:
        fd = open(args.config)
        config = yaml.load(fd.read())
        fd.close()
    else:
        config = {}

    # Load defaults
    fd = open(os.path.join(DATA_DIR, "default.yaml"))
    default_config = yaml.load(fd.read())
    fd.close()

    for key, val in default_config.items():
        if key not in config:
            config[key] = default_config[key]

    if "sawtooth_path" not in config:
        config["sawtooth_path"] = os.path.join(HOME_DIR, "sawtooth-core")

    # Store instance specific values
    config["owner"] = getpass.getuser()
    config["network_id"] = args.id

    config_file = os.path.join(get_dir(args.id), "config.yaml")
    fd = open(config_file, "w")
    fd.write(yaml.dump(config, default_flow_style=False))
    fd.close()


def load(network_id):
    config_file = os.path.join(get_dir(network_id), "config.yaml")
    try:
        fd = open(config_file)
        contents = yaml.load(fd.read())
        fd.close()
        return contents
    except FileNotFoundError as err:
        raise LrException("Unknown network, could not load config: {}".format(
            network_id))
