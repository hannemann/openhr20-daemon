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
        'stats_topic': 'stat/openhr20-python/RESULT/',
        'cmnd_topic': 'cmnd/openhr20-python/'
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
    }
}


def write_file():
    config.write(open(file, 'w'))
    print('Example config file written to %s.\nPlease adjust and restart.' % file)
    sys.stdout.flush()
    sys.exit(0)


if not os.path.exists(file):
    config['httpd'] = defaults['httpd']
    config['openhr20'] = defaults['openhr20']
    config['mqtt'] = defaults['mqtt']
    write_file()
else:
    config.read(file)
