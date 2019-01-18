from exceptions import LrException
import yaml
import os
import time

import sim.modules.load
import sim.modules.dev

MODULES = {
    'load': sim.modules.load,
    'restart': None,
    'ddos': None,
    'dev': sim.modules.dev,
}

def load(path_to_config):
    try:
        fd = open(path_to_config)
        contents = yaml.load(fd.read())
        fd.close()
        return contents
    except FileNotFoundError as err:
        raise LrException("Could not load timeline: {}".format(
            path_to_config))

def _raise_invalid(string, reason=""):
    raise LrException("Invalid time: {}. {}".format(string, reason))

def parse_time(string):
    try:
        digits = [int(s) for s in string.split(':')]
    except:
        _raise_invalid(string)

    if len(digits) != 4:
        _raise_invalid(string, "Must contain 4 digits.")

    days, hours, minutes, seconds = digits

    if not (24 > hours >= 0):
        _raise_invalid(string)
    if not (60 > minutes >= 0):
        _raise_invalid(string)
    if not (60 > seconds >= 0):
        _raise_invalid(string)

    hours += days * 24
    minutes += hours * 60
    seconds += minutes * 60

    return seconds


def _create_schedule(timeline):
    return sorted([
        (parse_time(etime), event) for etime, event in timeline.items()
    ], key=lambda tup: -tup[0])


def run(timeline, network_config):
    schedule = _create_schedule(timeline)
    t0 = time.time()
    procs = []

    started = 0
    exited = 0

    try:
        while len(schedule) > 0:
            i = 0
            while i < len(procs):
                p = procs[i]
                result = p.poll()
                if result is not None:
                    print("    ", p.pid, "exited with", result)
                    procs.remove(p)
                    exited += 1
                else:
                    print("  ", p.pid, "still sleeping...")
                    i += 1

            t = time.time() - t0

            etime, modules = schedule.pop()
            dt = etime - t

            if dt > 0:
                time.sleep(dt)

            for mod in modules:
                if mod in MODULES and MODULES[mod] is not None:
                    new_procs = MODULES[mod].run(modules[mod], network_config)
                    started += len(new_procs)
                    procs += new_procs

    except KeyboardInterrupt:
        print("Ctrl+C pressed, killing simulators!")
        for p in procs:
            print("  Killing ", p.pid)
            p.kill()

    finally:
        for p in procs:
            result = p.wait()
            exited += 1

        print("Started {}, {} exited".format(started, exited))
