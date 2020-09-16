import configparser
import os
import json
import time
from Device import Device


class Devices:

    AVAILABLE_WARN = 'warn'
    AVAILABLE_ONLINE = 'online'
    AVAILABLE_OFFLINE = 'offline'

    initialTimers = [
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '']
    ]

    def __init__(self):
        self.file = '/var/cache/openhr20/devices.conf'
        self.buffer = configparser.ConfigParser()
        self.last_sync = {}
        self.devices = {}

        if not os.path.exists(self.file):
            self.buffer['names'] = {
                '10': 'Livingroom',
                '11': 'Bathroom'
            }
            self.buffer['stats'] = {}
            self.buffer['timers'] = {}
            self.buffer['settings'] = {}
            self.buffer['groups'] = {}
        else:
            self.read()
        self.flush()

    def read(self):
        self.buffer.read(self.file)

        for addr in self.buffer['names']:
            device = Device(addr)
            device.time = int(time.time())
            device.set_availability()
            device.set_stats(json.loads(self.buffer.get('stats', str(addr), fallback='{"addr":%s}' % addr)))
            device.timers = json.loads(self.buffer.get('timers', str(addr), fallback=json.dumps(self.initialTimers)))
            device.settings = json.loads(self.buffer.get('settings', str(addr), fallback='{}'))
            device.group = self.get_group(addr)
            device.group_name = self.get_group_name(addr)
            device.name = self.buffer.get('names', addr)
            self.devices[addr] = device

    def flush(self):
        fd = open(self.file, 'w')
        for addr in self.buffer['names']:
            device = self.get_device(addr)
            self.buffer.set('stats', addr, str(device))
            self.buffer.set('settings', addr, json.dumps(device.settings))
            self.buffer.set('timers', addr, json.dumps(device.timers))
        self.buffer.write(fd)
        fd.close()
        print('Flushed devices to %s' % self.file)

    def get_group(self, addr):
        for name, group in dict(self.buffer['groups']).items():
            group = json.loads(group)
            if int(addr) in group:
                return group
        return None

    def get_group_name(self, addr):
        for name, group in dict(self.buffer['groups']).items():
            group = json.loads(group)
            if int(addr) in group:
                return name
        return None

    def get_devices_dict(self):
        devs = {}
        for addr in self.buffer['names']:
            device = self.get_device(addr)
            devs[int(addr)] = {
                'name': device.name,
                'stats': device.get_stats(),
                'timers': device.timers,
                'settings': device.settings,
                'group': device.group,
                'group_name': device.group_name,
            }
        return devs

    def has_device(self, addr):
        return True if str(addr) in self.devices else False

    def get_device(self, addr):
        return self.devices[str(addr)]


devices = Devices()
