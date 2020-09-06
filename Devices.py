import configparser
import os
import json

file = './devices.conf'
devices = configparser.ConfigParser()


def write_file():
    fd = open(file, 'w')
    devices.write(fd)
    fd.close()


def read_file():
    devices.read(file)


def get_devices_dict():
    read_file()
    devs = {}
    for addr in devices['names']:
        devs[int(addr)] = {
            'name': devices.get('names', addr),
            'stats': json.loads(devices.get('stats', addr, fallback='{}')),
            'timer': json.loads(devices.get('stats', addr, fallback='{}')),
            'settings': json.loads(devices.get('stats', addr, fallback='{}')),
        }
    return devs

if not os.path.exists(file):
    devices['names'] = {
        '10': 'Livingroom',
        '11': 'Bathroom'
    }
    devices['stats'] = {}
    devices['timer'] = {}
    devices['settings'] = {}

    write_file()
else:
    devices.read(file)
