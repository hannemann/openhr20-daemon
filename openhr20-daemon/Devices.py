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
        print('Read devices from {}'.format(self.file))

    def init_devices(self):
        for addr in self.buffer['names']:
            print('Init device {} {}'.format(addr, self.buffer.get('names', addr)))
            self.add_device(
                addr,
                self.buffer.get('names', addr),
                json.loads(self.buffer.get('stats', addr, fallback=self.get_initial_stats(addr))),
                json.loads(self.buffer.get('timers', addr, fallback=self.get_initial_timers())),
                json.loads(self.buffer.get('settings', addr, fallback='{}')),
                None
            )

    @staticmethod
    def get_initial_stats(addr):
        return '{{"addr":{}}}'.format(addr)

    @staticmethod
    def get_initial_timers():
        return json.dumps([[''] * 8] * 8)

    def add_device(self, addr, name, stats, timers, settings, group):
        self.devices[str(addr)] = Device(addr, name, stats, timers, settings, group)
        if group is not None:
            group.devices.append(self.devices[str(addr)])
            self.buffer.set('groups', group.key, json.dumps(group.dict()))
        self.buffer.set('names', str(addr), name)

    def remove_device(self, addr):
        device = self.get_device(addr)
        if device.group is not None:
            group = device.group
            group.remove(device)
            self.buffer.set('groups', group.key, json.dumps(group.dict()))
        del self.devices[str(addr)]
        self.buffer.remove_option('names', str(addr))
        self.buffer.remove_option('stats', str(addr))
        self.buffer.remove_option('timers', str(addr))
        self.buffer.remove_option('settings', str(addr))

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
        self.groups[key] = Group(key, name, devs)
        self.buffer.set('groups', key, json.dumps(self.groups[key].dict()))

    def remove_group(self, key):
        group = self.groups[key]
        for dev in group.devices:
            dev.group = None
        del self.groups[key]
        self.buffer.remove_option('groups', key)

    def add_device_to_group(self, addr, key):
        group = self.groups[key]
        device = self.get_device(addr)
        if device not in group.devices:
            group.append(device)
            device.group = self.groups[key]
            self.buffer.set('groups', key, json.dumps(group.dict()))

    def remove_device_from_group(self, addr, key):
        group = self.groups[key]
        device = self.get_device(addr)
        if device in group.devices:
            group.remove(device)
            device.group = None
            self.buffer.set('groups', key, json.dumps(group.dict()))

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
            print(' ! Flushed devices to {}'.format(self.file))
        except ValueError:
            print(' ! Refused to flush devices db. Devices empty...')

    def check(self):
        if os.path.exists(self.file) and len(self.buffer['names'].values()) == 0:
            raise ValueError

    def get_device(self, addr):
        return self.devices[str(addr)]

    def get_devices(self, with_remote=False):
        devs = self.devices.copy()
        if with_remote:
            for addr, remote in dict(self.buffer['remote_devices']).items():
                devs[addr] = self.get_device_from_remote(addr)
        return devs

    def get_groups(self, with_remote=False):
        grps = self.groups.copy()
        if with_remote:
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
            conn.request('GET', '/device/serialized/{}'.format(addr))
            device = pickle.loads(conn.getresponse().read())
            conn.close()
            return device
        else:
            raise KeyError

    def get_group_from_remote(self, name):
        remote = self.buffer.get('remote_groups', name, fallback=None)
        if remote is not None:
            conn = http.client.HTTPConnection(remote)
            conn.request('GET', '/group/serialized/{}'.format(name))
            group = pickle.loads(conn.getresponse().read())
            conn.close()
            return group
        else:
            raise KeyError

    def __str__(self, with_remote=False, groups=False):
        if groups:
            return json.dumps([g.dict() for g in self.get_groups(with_remote).values()])
        else:
            return json.dumps([d.dict() for d in self.get_devices(with_remote).values()])


devices = Devices()
