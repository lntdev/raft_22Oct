import os
import sys
import time
import subprocess


family, urls, rate, batch_size, src_dir, duration, key = sys.argv[1:]

def intkey(urls, rate, batch_size, src_dir, key):
    return [
        "{}/bin/intkey-workload".format(src_dir),
        "--rate", str(rate), "--urls", urls,
        "--key-file", key,
    ]

def smallbank(urls, rate, batch_size, src_dir, key):
    return [
        "{}/bin/smallbank-workload".format(src_dir), "load",
        "--rate", str(rate),
        "--max-batch-size", batch_size,
        "--target", urls,
        "--key", key,
    ]

FAMILY = {
    "intkey": intkey,
    "smallbank": smallbank,
}

args = FAMILY[family](urls, rate, batch_size, src_dir, key)

t = int(duration)

if t > 0:
    proc = subprocess.Popen(args)
    time.sleep(t)
    proc.kill()
    proc.wait()

else:
    subprocess.run(args)
