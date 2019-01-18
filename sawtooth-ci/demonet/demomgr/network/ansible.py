import os
import yaml

import network.config
import runner

from exceptions import LrException

ANSIBLE_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'ansible_data'
)


def get_node_ip(node, network_id):
    instance_tag = "tag_Name_{}_node{}".format(network_id, node)

    cwd = os.getcwd()
    os.chdir(ANSIBLE_PATH)

    instances = yaml.load(runner.run(
        ['./ec2.py', '--list'],
        capture_stdout=True
    ))

    os.chdir(cwd)
    
    if instance_tag in instances:
        if len(instances[instance_tag]) > 0:
            return instances[instance_tag][0]

    raise LrException("Instance tag not found: {}".format(instance_tag))


def get_name_tag(node, network_id):
    return "tag_Name_{}_node{}".format(network_id, node)


def get_network_tag(network_id):
    return "tag_Network_{}".format(network_id)


def playbook(name, config, extra_vars=None, retries=0, delay=0, delay_factor=1):
    """Playbook must be located in ansible_data/playbooks"""
    playbook = _get_playbook_args(name, config, extra_vars)

    cwd = os.getcwd() # Need this to use ansible.cfg
    os.chdir(ANSIBLE_PATH)
    print("Running {}".format(playbook))
    runner.run(playbook,
        retries=retries, delay=delay, delay_factor=delay_factor)
    os.chdir(cwd)
    


def _get_playbook_args(playbook, config, extra_vars=None):
    network_tag = get_network_tag(config['network_id'])

    args = [
        "ansible-playbook", "--user={}".format(config['host_user']),
        "--private-key={}".format(config['key_file']),
        "playbooks/{}.yaml".format(playbook),
        "-i", "ec2.py", "-e", "network_name={}".format(network_tag)
    ]

    if extra_vars is not None:
        for evar in extra_vars:
            args += ["-e", evar]

    return args
