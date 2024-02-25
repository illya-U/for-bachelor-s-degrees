import os
import sys


def get_cred():
    config = {}
    with open(os.path.join(sys.path[0], "cred.txt"), "r") as conf_file:
        for cred in conf_file:
            try:
                key, value = cred.split(" = ")
            except ValueError:
                continue
            config.update({key: value.strip()})
    return config
