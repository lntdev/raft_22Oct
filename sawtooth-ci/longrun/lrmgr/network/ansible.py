import os
import yaml

import network.config
import runner
import network.terraform as tf

from exceptions import LrException

ANSIBLE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'ansible_data'
)


def get_name_tag(node, network_id):
    return "tag_Name_{}_node{}".format(network_id, node)


def get_network_tag(network_id):
    return "tag_Network_{}".format(network_id)


def playbook(name, config, playbook_args=None, retries=0, delay=0, delay_factor=1):
    """Playbook must be located in ansible_data/playbooks"""

    extra_vars = [
        "genesis_tag='{}'".format(
            get_name_tag(0, config['network_id'])
        ),
        "genesis_ip='{}'".format(
            tf.get_node_ip(0, config)
        ),
        "sawtooth_packages='{}'".format(config['sawtooth_packages']),
        "sawtooth_version='{}'".format(config['sawtooth_version']),
        "sawtooth_services='{}'".format(config['sawtooth_services']),
        "sawtooth_configs='{}'".format(config['sawtooth_configs']),
        "sawtooth_repo='{}'".format(config['sawtooth_repo']),
        "influx_url='{}'".format(config['influx_url']),
        "influx_database='metrics_{}'".format(config['network_id']),
#        "influx_username='{}'".format(os.environ['INFLUX_USERNAME']),
#        "influx_password='{}'".format(os.environ['INFLUX_PASSWORD']),
        "syslog_server='{}'".format(config['syslog_server']),
        "syslog_port='{}'".format(config['syslog_port']),
        "max_batches_per_block='{}'".format(config['max_batches_per_block']),
        "scheduler='{}'".format(config['scheduler']),
    ]

    if playbook_args is not None:
        extra_vars.extend(playbook_args)

    playbook = _get_playbook_args(name, config, extra_vars)

    cwd = os.getcwd() # Need this to use ansible.cfg
    os.chdir(ANSIBLE_PATH)
    print("Running `%s`" % " ".join(playbook))
    runner.run(playbook,
        retries=retries, delay=delay, delay_factor=delay_factor)
    os.chdir(cwd)
    


def _get_playbook_args(playbook, config, extra_vars=None):
    network_tag = get_network_tag(config['network_id'])

    args = [
        "ansible-playbook", "--user={}".format(config['host_user']),
        "--private-key={}".format(config['key_file']),
        "playbooks/{}.yaml".format(playbook),
        "-i", "ec2.py", "-e", "network_name={}".format(network_tag),
        "-e", "ansible_python_interpreter=/usr/bin/python3"
    ]

    if extra_vars is not None:
        for evar in extra_vars:
            args += ["-e", evar]

    return args
