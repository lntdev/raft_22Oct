import yaml
import os

SIM_DIR = os.path.join(os.path.expanduser("~"), ".lrmgr", "sim")
DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')


def create_dir(sim_id):
    sim_dir = get_dir(sim_id)
    try:
        if not os.path.exists(sim_dir):
            os.makedirs(sim_dir)
    except OSError:
        raise LrException("Failed to create directory: {}".format(sim_id))


def get_dir(sim_id):
    return "{}/{}".format(SIM_DIR, sim_id)


def load(path_to_config):
    try:
        fd = open(path_to_config)
        contents = yaml.load(fd.read())
        fd.close()
        return contents
    except FileNotFoundError as err:
        raise LrException("Could not load sim config: {}".format(
            path_to_config))
