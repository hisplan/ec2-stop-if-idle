#!/usr/bin/env python

import time
import subprocess

def run_command(cmd, shell=False, strip_newline=True):
    "run a command and return (stdout, stderr, exit code)"

    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell
    )

    stdout, stderr = process.communicate()

    stdout = stdout.decode()
    stderr = stderr.decode()

    if strip_newline:
        stdout = stdout.rstrip("\n")
        stderr = stderr.rstrip("\n")

    return stdout, stderr, process.returncode



instance_id, _, _ = run_command(["curl", "http://169.254.169.254/latest/meta-data/instance-id"])

print(instance_id)

while True:

    stdout, stderr, return_code = run_command(["ps", "-p", "4398", "-o", "%cpu,%mem", "--no-headers"])

    cpu, _, mem = stdout.split(" ")

    cpu = float(cpu)
    mem = float(mem)

    print(cpu, mem)

    if cpu > 20:
        break

    time.sleep(1)


print("stop")



