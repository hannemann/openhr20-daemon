import configparser
import os
import sys
from dotenv import load_dotenv
load_dotenv(override=True)


file = os.getenv("CONFIG_FILE")
config = configparser.ConfigParser()
defaults = {
    'httpd': {
        'host': '0.0.0.0',
        'port': 8020
    },
    'ws': {
        'listen_address': '0.0.0.0',
        'scheme': 'ws',
        'host': '0.0.0.0',
        'port': 8021
    },
    'mqtt-modes-receive': {'auto': 'auto', 'manu': 'manu'},
    'mqtt-modes-publish': {'auto': 'auto', '-': 'auto', 'manu': 'manu'},
    'mqtt-presets-receive': {'antifreeze': 'antifreeze', 'eco': 'eco', 'comfort': 'comfort', 'supercomfort': 'supercomfort'},
    'mqtt-presets-publish': {'antifreeze': 'antifreeze', 'eco': 'eco', 'comfort': 'comfort', 'supercomfort': 'supercomfort'}
}


def write_file():
    config.write(open(file, 'w'))
    print('Example config file written to %s.\nPlease adjust and restart.' % file)
    sys.stdout.flush()
    sys.exit(0)


if not os.path.exists(file):
    config['httpd'] = defaults['httpd']
    config['ws'] = defaults['ws']
    config['mqtt'] = defaults['mqtt']
    config['mqtt-modes-receive'] = defaults['mqtt-modes-receive']
    config['mqtt-modes-send'] = defaults['mqtt-modes-publish']
    config['mqtt-presets-receive'] = defaults['mqtt-presets-receive']
    config['mqtt-presets-send'] = defaults['mqtt-presets-publish']
    write_file()
else:
    config.read(file)
