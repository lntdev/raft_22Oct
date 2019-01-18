import os
import sys
import time
import subprocess


url, rate, src_dir, workload, duration = sys.argv[1:]

path = ":".join([
    "{0}/core",
    "{0}/validator",
    "{0}/docs",
    "{0}/tools",
    "{0}/signing",
    "{0}/signing/build/lib.linux-x86_64-2.7",
    "{0}/core/build/lib.linux-x86_64-2.7",
    "{0}/validator/build/lib.linux-x86_64-2.7",
    "{0}/extensions/bond"
]).format(src_dir)
os.environ['PYTHONPATH'] = path

args = [
    "python2", "{}/bin/simulator".format(src_dir),
    "--url", url,
    "--rate", str(rate),
    "--workload", workload
]

t = int(duration)

if t > 0:
    proc = subprocess.Popen(args)
    time.sleep(t)
    proc.kill()
    proc.wait()

else:
    subprocess.run(args)
