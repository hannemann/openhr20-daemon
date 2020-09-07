import configparser
import os
import sys


file = '/etc/openhr20/daemon.conf'
config = configparser.ConfigParser()


def write_file():
    config.write(open(file, 'w'))
    print('Example config file written to %s.\nPlease adjust and restart.' % file)
    sys.stdout.flush()
    sys.exit(0)


if not os.path.exists(file):
    config['openhr20'] = {
        'master': '/dev/ttyUSB0',
        'baud': 38400,
        'timeout': 1,
        'debug': False
    }
    config['mqtt'] = {
        'host': 'heimomat',
        'port': 1883,
        'qos': 0,
        'retain': 'no',
        'stats_topic': 'stat/openhr20-python/RESULT/',
        'cmnd_topic': 'cmnd/openhr20-python/'
    }

    write_file()
else:
    config.read(file)
