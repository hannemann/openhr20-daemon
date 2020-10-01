import configparser
import pickle
import http.client
import os
import json
from Device import Device
from Group import Group


class Devices:

    def __init__(self):
        self.file = os.getenv("DEVICES_FILE")
        self.buffer = configparser.ConfigParser()
        self.devices = {}
        self.groups = {}

        if not os.path.exists(self.file):
            self.buffer['names'] = {}
            self.buffer['stats'] = {}
            self.buffer['timers'] = {}
            self.buffer['settings'] = {}
            self.buffer['groups'] = {}
            self.buffer['remote_groups'] = {}
            self.buffer['remote_devices'] = {}
            self.flush()
        else:
            self.buffer.read(self.file)

        self.init_devices()
        self.init_groups()
        print('Read devices from %s' % self.file)

    def init_devices(self):
        for addr in self.buffer['names']:
            self.add_device(
                addr,
                self.buffer.get('names', addr),
                json.loads(self.buffer.get('stats', addr, fallback='{"addr":%s}' % addr)),
                json.loads(self.buffer.get('timers', addr, fallback=json.dumps([[''] * 8] * 8))),
                json.loads(self.buffer.get('settings', addr, fallback='{}')),
                None
            )

    def add_device(self, addr, name, stats, timers, settings, group):
        self.devices[addr] = Device(addr, name, stats, timers, settings, group)
        self.buffer.set('names', addr, name)

    def remove_device(self, addr):
        del self.devices[addr]
        self.buffer.remove_option('names', addr)

    def add_remote_device(self, addr, host, port):
        self.buffer.set('remote_devices', str(addr), '{}:{}'.format(host, port))

    def remove_remote_device(self, addr):
        self.buffer.remove_option('remote_devices', addr)

    def init_groups(self):
        groups = dict(self.buffer['groups'])
        for key, group in groups.items():
            group = json.loads(group)
            devs = [d for d in self.devices.values() if d.addr in [d for d in group['devices']]]
            self.add_group(key, group['name'], devs)
            for device in devs:
                device.group = self.groups[key]

    def add_group(self, key, name, devs):
        self.groups[key] = Group(name, devs)
        self.buffer.set('groups', key, json.dumps(self.groups[key].dict()))

    def remove_group(self, key):
        del self.groups[key]
        self.buffer.remove_option('groups', key)

    def add_remote_group(self, key, host, port):
        self.buffer.set('remote_groups', key, '{}:{}'.format(host, port))

    def remove_remote_group(self, key):
        self.buffer.remove_option('remote_groups', key)

    def flush(self):
        try:
            self.check()
            for addr in self.buffer['names']:
                device = self.get_device(addr)
                self.buffer.set('stats', addr, str(device))
                self.buffer.set('settings', addr, json.dumps(device.settings))
                self.buffer.set('timers', addr, json.dumps(device.timers))
            fd = open(self.file, 'w')
            self.buffer.write(fd)
            fd.close()
            print('Flushed devices to %s' % self.file)
        except ValueError:
            print('Refused to flush devices db. Devices empty...')

    def check(self):
        if os.path.exists(self.file) and len(self.buffer['names'].values()) == 0:
            raise ValueError

    def get_device(self, addr):
        return self.devices[str(addr)]

    def get_devices(self):
        devs = self.devices.copy()
        for addr, remote in dict(self.buffer['remote_devices']).items():
            devs[addr] = self.get_device_from_remote(addr)
        return devs

    def get_groups(self):
        grps = self.groups.copy()
        for name, remote in dict(self.buffer['remote_groups']).items():
            grps[name] = self.get_group_from_remote(name)
        return grps

    def get_remote(self, addr):
        return self.buffer.get('remote_devices', str(addr), fallback=None)

    def is_remote_device(self, addr):
        return str(addr) in dict(self.buffer['remote_devices'])

    def get_device_from_remote(self, addr):
        remote = self.get_remote(addr)
        if remote is not None:
            conn = http.client.HTTPConnection(remote)
            conn.request('GET', '/device/serialized/%s' % addr)
            device = pickle.loads(conn.getresponse().read())
            conn.close()
            return device
        else:
            raise KeyError

    def get_group_from_remote(self, name):
        remote = self.buffer.get('remote_groups', name, fallback=None)
        if remote is not None:
            conn = http.client.HTTPConnection(remote)
            conn.request('GET', '/group/serialized/%s' % name)
            group = pickle.loads(conn.getresponse().read())
            conn.close()
            return group
        else:
            raise KeyError


devices = Devices()
