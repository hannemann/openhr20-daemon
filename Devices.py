import configparser
import os
import json

file = '/var/cache/openhr20/devices.conf'
devices = configparser.ConfigParser()


def write_file():
    fd = open(file, 'w')
    devices.write(fd)
    fd.close()


def read_file():
    devices.read(file)


def get_device_settings(addr):
    return json.loads(devices.get('settings', str(addr), fallback='{}'))


def set_device_settings(addr, settings):
    devices.set('settings', str(addr), json.dumps(settings))


def get_devices_dict():
    devs = {}
    for addr in devices['names']:
        devs[int(addr)] = {
            'name': devices.get('names', addr),
            'stats': json.loads(devices.get('stats', addr, fallback='{}')),
            'timer': json.loads(devices.get('timer', addr, fallback='{}')),
            'settings': get_device_settings(addr),
        }
    return devs


def set_synced(addr, synced):
    if str(addr) in devices['stats']:
        stats = json.loads(devices.get('stats', str(addr)))
        stats['synced'] = synced
        devices.set('stats', str(addr), json.dumps(stats))


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
