import os
import json


def get_config_default(file):
    try:
        with open(file) as fd:
            return json.load(fd)

    except OSError:
        with open(file, "w") as fd:
            config = {
                "ssid": "default network",
                "password": "default password",
            }
            print("Writing config: {config}")
            json.dump(config, fd)
            return config
    
def set_config(file, config):
    try:
        with open(file, "w") as fd:
            json.dump(config, fd)
    except OSError:
        print("Failed to write config")
