import subprocess
import time

from exceptions import LrException


def run(args, capture_stdout=False, retries=0, delay=0, delay_factor=1):
    while retries >= 0:
        try:
            return _run(args, capture_stdout)

        except LrException as err:
            if retries > 0:
                print(
                    "Command failed. Retries left: {}. "
                    "Retrying in {}sec...".format(retries, delay)
                )
                time.sleep(delay)
                delay *= delay_factor
                retries -= 1 
            else:
                raise err


def spawn(args):
    return subprocess.Popen(args)
            

def _run(args, capture_stdout):
    try:
        if capture_stdout:
            process = subprocess.run(
                args, stdout=subprocess.PIPE,
                check=True
            )

            return process.stdout.decode()
        else:
            process = subprocess.run(args, check=True)
            return ""

    except subprocess.CalledProcessError as err:

        raise LrException("Failed to execute subprocess, exit code: {}"
            "`{}`".format(err.returncode, args)
        )
