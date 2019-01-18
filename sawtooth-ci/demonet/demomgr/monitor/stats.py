import yaml
import urllib.request
from urllib.error import URLError

import network.terraform as tf
import monitor.divergence


def post(url, data):
    cereal = yaml.dump(data).encode()
    request = urllib.request.Request(url, cereal)
    try:
        result = urllib.request.urlopen(request)
        print("Result: {}".format(result.read().decode()))
    except URLError:
        print("Failed to log stats {}".format(data))


def get(config):
    ips = tf.get_network_ips(config)    
    stats = {}

    for ip in ips:
        stats[ip] = _get_stats(ip)

    # TODO: Compute aggregate stats
    # - Txn Rate is averaged, need to store time/count somehow
    stats = _add_aggregate_stats(stats)

    return stats


def _add_aggregate_stats(stats):
    memory_used = 0
    cpu_used = 0
    blocks = 0
    transactions = -1
    divergence = -1

    try:
        transactions = max(
            node['journal']['CommittedTxnCount'] for node in stats.values()
        )
        blocks = max(
            node['journal']['CommittedBlockCount'] for node in stats.values()
        )
        memory_used = max(
            node['platform']['svmem']['used'] for node in stats.values()
        )
        cpu_used = max(
            node['platform']['scpu']['percent'] for node in stats.values()
        )
    except:
        print("Failed to aggregate platform and journal stats")

    try:
        divergence = monitor.divergence.get(stats)
    except:
        print("Failed to calculate divergence")

    stats['all'] = {
        'mem': memory_used,
        'cpu': cpu_used,
        'blocks': blocks,
        'transactions': transactions,
        'divergence': divergence,
    }

    return stats


def _get_stats(ip):
    val_stats = _get_validator_stats(ip) 
    block_stats =_get_block_info(ip)

    if val_stats['response'] == 'yes' and block_stats['response'] == 'yes':
        stats = _process_stats(val_stats['data'], block_stats['data'])

    else:
         stats = {}
    
    return stats


def _get_block_info(ip):
    return _get_request("http://{}:8800/block?blockcount=5&info=1".format(ip))


def _get_validator_stats(ip):
    return _get_request("http://{}:8800/statistics/all".format(ip))


def _process_stats(val_stats, block_stats):
    platform = val_stats['platform']
    journal = val_stats['journal']
    try:
        val_stats['block_history'] = block_stats
        return val_stats
    except KeyError:
        return {}

def _get_request(url):
    try:
        print("Getting {}".format(url))
        request = urllib.request.Request(url)
        result = urllib.request.urlopen(request).read().decode()
    except URLError:
        return {'response': 'no', 'data': None}

    try:
        data = yaml.load(result)
    except yaml.YAMLError:
        return {'response': 'bad', 'data': result} 

    return {'response': 'yes', 'data': data}
