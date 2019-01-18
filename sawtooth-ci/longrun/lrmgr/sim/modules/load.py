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
FAMILIES = ["intkey", "smallbank"]


def run(args, network_config):
    print("Load: {}, {}".format(args, network_config))
    procs = []

    if 'family' not in args:
        raise LrException("No family specified for load command")
    else:
        family = args['family']
        if family not in FAMILIES:
            raise LrException("Unkown load family: {}".format(family))

    if 'sawtooth_path' in network_config:
        src_dir = network_config['sawtooth_path']
        if not os.path.exists(src_dir):
            raise LrException("Sawtooth not found at: {}".format(src_dir))
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
                "Duration {} is invalid".format(args['duration'])
            )
    else:
        duration = -1

    if 'transactor_key' not in args:
        raise LrException("No transactor signing key specified")

    key = args['transactor_key']

    if 'rate' not in args:
        raise LrException("No rate specified")

    try:
        rate = int(args['rate'])
    except:
        raise LrException("Rate {} is invalid".format(args['rate']))

    if 'batch_size' in args:
        if family != 'smallbank':
            raise LrException("Batch size only supported in smallbank")
        batch_size = int(args['batch_size'])
    else:
        batch_size = 1

    urls = ",".join([
        "http://{}:8080".format(tf.get_node_ip(node, network_config))
        for node in args['nodes']
    ])

    print("Starting {} workload: {} TPS => {} for {} seconds...".format(
        family, rate, urls, duration))

    procs.append(
        runner.spawn([
            PYTHON, HELPER, family, urls, str(rate), str(batch_size), src_dir, str(duration), key
        ])
    )

    return procs
