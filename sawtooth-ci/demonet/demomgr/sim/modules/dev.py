import os
import sys
import random
import subprocess

import runner
import network.terraform as tf
import network.config

PYTHON = sys.executable
HELPER = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), 
    "helpers", "dev.py")

def run(args, network_config):
    procs = []

    n = random.randint(2,4)

    while n > 0:
        t = random.randint(1,5)
        p = subprocess.Popen([PYTHON, HELPER, str(t)])
        print("{} sleeping for {}".format(p.pid, t))
        procs.append(p)
        n -= 1

    return procs
