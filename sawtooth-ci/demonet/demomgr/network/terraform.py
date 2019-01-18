import os

import yaml
import network.config
import runner
from exceptions import LrException 

TF_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
    'tf_data'
)


def create(network_config):
    env_vars = _create_env_vars(network_config)
    state_flag = _create_state_flag(network_config)
    
    cwd = os.getcwd()
    os.chdir(TF_PATH)

    new = _state_exists(network_config)

    # Create
    if not new:
        runner.run(
            ['terraform', 'apply'] + env_vars + state_flag,
            retries=3, delay=15, delay_factor=2
        )


    # Convert ips to csv
    ips = ",".join([
        "{}/32".format(ip) for ip in get_network_ips(network_config)
    ])

    # Create ingress from ips
    runner.run(
        ['terraform', 'apply'] + env_vars + state_flag + 
        ['--var', 'validator_ingress={}'.format(ips)],
        retries=3, delay=15, delay_factor=2
    )

    os.chdir(cwd)


def destroy(network_config):
    env_vars = _create_env_vars(network_config)
    state_flag = _create_state_flag(network_config)

    cwd = os.getcwd()
    os.chdir(TF_PATH)

    # Destory
    runner.run(['terraform', 'destroy'] + env_vars + state_flag + ['--force'])

    os.chdir(cwd)


def _get_output(network_config):
    state_flag = _create_state_flag(network_config)

    # Get ips
    return yaml.load(runner.run(
        ['terraform', 'output', '-json'] + state_flag,
        capture_stdout=True
    ))


def get_network_ips(network_config):
    return _get_output(network_config)['ips']['value']


def get_node_name(node, network_config):
    return "{}-node{}".format(network_config['network_id'], node)
    

def get_node_ip(node, network_config):
    output = _get_output(network_config)
    node_name = get_node_name(node, network_config)
    i = 0
    for node in output['tags']['value']:
        if node['Name'] == node_name:
            return output['ips']['value'][i]
        i += 1
    raise LrException("Node `{}` not found.".format(node_name))


def _create_env_vars(config):
    return [
        '--var', 'network_id={}'.format(config['network_id']),
        '--var', 'environment={}'.format(config['environment']),
        '--var', 'host_user={}'.format(config['host_user']),
        '--var', 'owner={}'.format(config['owner']),
        '--var', 'region={}'.format(config['region']),
        '--var', 'count={}'.format(config['count']),
        '--var', 'ami={}'.format(config['image_id']),
        '--var', 'instance_type={}'.format(config['instance_type']),
    ]


def _state_exists(config):
    return os.path.exists(os.path.join(
        network.config.get_dir(config['network_id']), 
        'terraform.tfstate'
    ))


def _create_state_flag(config):
    return ['-state={}'.format(
        os.path.join(
            network.config.get_dir(config['network_id']), 
            'terraform.tfstate'
        )
    )]
