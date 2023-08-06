#!/usr/bin/python3
import re
import subprocess
import sys
from threading import Thread

import yaml


def open_file(filepath):
    try:
        with open(filepath) as f:
            return f.read()
    except OSError as e:
        print(
            f"Cannot open config with path: {filepath}, error: {e.strerror}",
            file=sys.stderr,
        )
        exit(2)


def run_probe(probe_name, command):
    result = subprocess.run(command, text=True, capture_output=True)
    search = re.search(r" - .*", result.stdout)
    if search:
        print(f"{result.returncode} {probe_name} {search.group()}")
    else:
        print(f"{result.returncode} {probe_name} - {result.stdout}")
    return result.returncode


def main(config_filepath):
    config = yaml.safe_load(open_file(config_filepath))
    if not config:
        return

    for _, options in config.items():
        module = options["module"]
        for name, args in options.get("runs").items():
            command = ["python", "-m", module]
            for arg_name, arg_val in args.items():
                if len(arg_name) == 1:
                    arg_name = "-" + arg_name
                else:
                    arg_name = "--" + arg_name
                if arg_val is True:
                    arg_val = "true"
                elif arg_val is False:
                    arg_val = "false"
                command.append(arg_name)
                command.append(str(arg_val))
            Thread(target=run_probe, args=[name, command]).start()


if __name__ == "__main__":
    config_filepath = "/etc/run_probes_cfg.yaml"
    main(config_filepath)
