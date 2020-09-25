import configparser
import os
import sys


file = '/etc/openhr20/daemon.conf'
config = configparser.ConfigParser()
defaults = {
    'mqtt': {
        'host': 'mqtt.example.com',
        'port': 1883,
        'qos': 0,
        'retain': False,
        'stats_topic': 'stat/openhr20/RESULT/',
        'cmnd_topic': 'cmnd/openhr20/',
        'availability_topic': 'stat/openhr20/AVAILABLE/'
    },
    'openhr20': {
        'master': '/dev/ttyUSB0',
        'baud': 38400,
        'timeout': 1,
        'device-db': '/var/cache/openhr20/devices.db'
    },
    'httpd': {
        'host': '0.0.0.0',
        'port': 8020
    },
    'ws': {
        'host': '0.0.0.0',
        'port': 8021
    },
    'mqtt-modes-receive': {
        'auto': 'auto',
        'manu': 'manu'
    },
    'mqtt-modes-publish': {
        'auto': 'auto',
        '-': 'auto',
        'manu': 'manu'
    },
    'mqtt-presets-receive': {
        'antifreeze': 'antifreeze',
        'eco': 'eco',
        'comfort': 'comfort',
        'supercomfort': 'supercomfort',
    },
    'mqtt-presets-publish': {
        'antifreeze': 'antifreeze',
        'eco': 'eco',
        'comfort': 'comfort',
        'supercomfort': 'supercomfort',
    }
}


def write_file():
    config.write(open(file, 'w'))
    print('Example config file written to %s.\nPlease adjust and restart.' % file)
    sys.stdout.flush()
    sys.exit(0)


if not os.path.exists(file):
    config['httpd'] = defaults['httpd']
    config['ws'] = defaults['ws']
    config['openhr20'] = defaults['openhr20']
    config['mqtt'] = defaults['mqtt']
    config['mqtt-modes-receive'] = defaults['mqtt-modes-receive']
    config['mqtt-modes-send'] = defaults['mqtt-modes-publish']
    config['mqtt-presets-receive'] = defaults['mqtt-presets-receive']
    config['mqtt-presets-send'] = defaults['mqtt-presets-publish']
    write_file()
else:
    config.read(file)
