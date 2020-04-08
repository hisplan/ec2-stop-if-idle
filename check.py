#!/usr/bin/env python

import time
import subprocess
import datetime
import re
import argparse
import sys


def run_command(cmd, shell=False):
    "run a command and return (stdout, stderr, exit code)"

    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell
    )

    stdout, stderr = process.communicate()

    stdout = stdout.decode().strip()
    stderr = stderr.decode().strip()

    return stdout, stderr, process.returncode


def main(pid, threshold_cpu, check_frequency, dry_run):

    print("CPU threshold: {}%".format(threshold_cpu))

    instance_id, _, _ = run_command(["curl", "http://169.254.169.254/latest/meta-data/instance-id"])

    print(instance_id)

    hits = 0

    while True:

        stdout, _, return_code = run_command(["ps", "-p", str(pid), "-o", "%cpu,%mem", "--no-headers"])

        now = str(datetime.datetime.now())

        if return_code == 0:

            try:
                match = re.search(r"^(.*?)\s+(.*?)$", stdout)
                if not match:
                    raise Exception("The output of ps is not something expected!")

                cpu = match.group(1)
                mem = match.group(2)

                cpu = float(cpu)
                mem = float(mem)

                if cpu < threshold_cpu:
                    hits += 1

                print("{0} CPU={1:3.1f}% MEM={2:3.1f}% HITS={3}".format(now, cpu, mem, hits))

            except Exception as ex:
                print(str(ex))
                print(stdout)
                sys.exit(1)

        else:

            # looks like the process has been terminated/killed
            hits += 1

            print("{} CPU=n/a MEM=n/a HITS={}".format(now, hits))

        if hits == 5:
            break

        # in seconds
        time.sleep(check_frequency)

    if dry_run:
        print("Will not stop the instance because this is a dry run.")
        exit(0)
    else:
        print("Will stop the instance after 1 minute")

    time.sleep(60)

    run_command(["aws", "ec2", "stop-instances", "--instance-ids", instance_id])




def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--pid",
        action="store",
        dest="pid",
        help="ID of the process you'd like to monitor",
        type=int,
        required=True
    )

    parser.add_argument(
        "--cpu",
        action="store",
        dest="threshold_cpu",
        help="will stop the instance if the CPU utilization is below this percentage (e.g. 1)",
        default=1.0,
        type=float,
        required=False
    )

    parser.add_argument(
        "--frequency",
        action="store",
        dest="check_frequency",
        help="how often to check the CPU and memory usage (in secodns)",
        default=60,
        type=int,
        required=False
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        dest="dry_run",
        help="Dry run (won't stop the instance even if the conditions are satisfied)",
        required=False
    )

    # parse arguments
    params = parser.parse_args()

    return params


if __name__ == "__main__":

    params = parse_arguments()

    main(
        params.pid,
        params.threshold_cpu,
        params.check_frequency,
        params.dry_run
    )
