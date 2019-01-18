import os
import sys

import runner
import network.terraform as tf
import network.config
import sim.timeline

from exceptions import LrException

PYTHON = sys.executable
HELPER = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 
    "helpers", "load.py")
FAMILY = {
    "intkey": "txnintegration.integer_key_workload.IntegerKeyWorkload",
    "bond": "sawtooth_bond.bond_workload.BondWorkload",
}


def run(args, network_config):
    print("got {}, {}".format(args, network_config))
    procs = []

    if 'family' in args:
        if args['family'] not in FAMILY:
            raise LrException("Unkown load family: {}".format(family))
        family = FAMILY[args['family']]

    else:
        family = FAMILY['intkey']

    if 'sawtooth_path' in network_config:
        src_dir = network_config['sawtooth_path']
        if not os.path.exists(src_dir):
            raise LrException("Sawtooth not found at: {}", src_dir)
    else:
        raise LrException(
            "Network config does not contain `sawtooth_path`."
            " Cannot load without access to sawtooth-core."
        )

    if 'duration' in args:
        try:
            duration = sim.timeline.parse_time(args['duration'])
        except:
            raise LrException(
                "Duration must be integral, {} is invalid".format(duration)
            )
    else:
        duration = -1

    for node in args['nodes']:
        node_url = "http://{}:8800".format(
            tf.get_node_ip(node, network_config))

        rate = args['nodes'][node]

        print("Starting {} workload: {} TPM => {} for {} seconds...".format(
            family, rate, node_url, duration))

        procs.append(
            runner.spawn([
                PYTHON, HELPER, node_url, str(rate), src_dir, family, str(duration)
            ])
        )

    return procs
