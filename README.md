# ec2-stop-if-idle

```bash
$ python check.py  --help
usage: check.py [-h] --pid PID [--cpu THRESHOLD_CPU]
                [--frequency CHECK_FREQUENCY] [--dry-run]

optional arguments:
  -h, --help            show this help message and exit
  --pid PID             ID of the process you'd like to monitor
  --cpu THRESHOLD_CPU   will stop the instance if the CPU utilization is below
                        this percentage (e.g. 1)
  --frequency CHECK_FREQUENCY
                        how often to check the CPU and memory usage (in
                        secodns)
  --dry-run             Dry run (won't stop the instance even if the
                        conditions are satisfied)
```

```bash
$ screen -S monitor
$ python check.py --pid 3118 --frequency=60 --cpu 1 | tee monitor.log
```


