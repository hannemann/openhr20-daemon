import configparser
import pickle
import http.client
import os
import json
from Device import Device
from Group import Group
from Config import config, defaults
import copy


class Devices:

    def __init__(self):
        self.file = config.get('openhr20', 'device-db', fallback=defaults['openhr20']['device-db'])
        self.buffer = configparser.ConfigParser()
        self.devices = {}
        self.groups = {}

        if not os.path.exists(self.file):
            self.buffer['names'] = {
                '10': 'Livingroom',
                '11': 'Bathroom'
            }
            self.buffer['stats'] = {}
            self.buffer['timers'] = {}
            self.buffer['settings'] = {}
            self.buffer['groups'] = {}
            self.buffer['proxy_groups'] = {}
            self.buffer['proxy_devices'] = {}
            self.flush()
        else:
            self.buffer.read(self.file)
            self.init_devices()
            self.init_groups()
            print('Read devices from %s' % self.file)

    def init_devices(self):
        for addr in self.buffer['names']:
            try:
                groups = dict(self.buffer['groups'])
                group = json.loads([group for group in groups.values() if int(addr) in json.loads(group)['devices']][0])
            except IndexError:
                group = None
            device = Device(
                addr,
                self.buffer.get('names', addr),
                json.loads(self.buffer.get('stats', addr, fallback='{"addr":%s}' % addr)),
                json.loads(self.buffer.get('timers', addr, fallback=json.dumps([[''] * 8] * 8))),
                json.loads(self.buffer.get('settings', addr, fallback='{}')),
                None
            )
            self.devices[addr] = device

    def init_groups(self):
        groups = dict(self.buffer['groups'])
        for key, group in groups.items():
            group = json.loads(group)
            devs = [d for d in self.devices.values() if d.addr in [d for d in group['devices']]]
            self.groups[key] = Group(group['name'], devs)
            for device in devs:
                device.group = self.groups[key]


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

    def get_device(self, addr):
        return self.devices[str(addr)]

    def get_devices(self):
        devs = self.devices.copy()
        for addr, proxy in dict(self.buffer['proxy_devices']).items():
            devs[addr] = self.get_device_from_proxy(addr)
        return devs

    def get_groups(self):
        grps = self.groups.copy()
        for name, proxy in dict(self.buffer['proxy_groups']).items():
            grps[name] = self.get_group_from_proxy(name)
        return grps

    def get_proxy(self, addr):
        return self.buffer.get('proxy_devices', str(addr), fallback=None)

    def has_proxy(self, addr):
        return str(addr) in dict(self.buffer['proxy_devices'])

    @staticmethod
    def get_device_from_proxy(addr):
        proxy = devices.buffer.get('proxy_devices', str(addr), fallback=None)
        if proxy is not None:
            conn = http.client.HTTPConnection(proxy)
            conn.request('GET', '/device/serialized/%s' % addr)
            device = pickle.loads(conn.getresponse().read())

            device.group = None

            conn.close()
            return device
        else:
            raise KeyError

    @staticmethod
    def get_group_from_proxy(name):
        proxy = devices.buffer.get('proxy_groups', name, fallback=None)
        if proxy is not None:
            conn = http.client.HTTPConnection(proxy)
            conn.request('GET', '/group/serialized/%s' % name)
            group = pickle.loads(conn.getresponse().read())
            conn.close()
            return group
        else:
            raise KeyError


devices = Devices()
