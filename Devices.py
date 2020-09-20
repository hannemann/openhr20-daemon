import configparser
import os
import json
from Device import Device
from Group import Group
from Config import config, defaults


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
                group
            )
            self.devices[addr] = device

    def init_groups(self):
        for addr, device in self.devices.items():
            if device.group is not None:
                if device.group['name'] not in self.groups:
                    group = device.group
                    group = Group(
                        group['name'],
                        [d for d in self.devices.values() if d.addr in [d for d in group['devices']]]
                    )
                    device.group = group
                    self.groups[group.name] = group
                else:
                    device.group = self.groups[device.group['name']]

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


devices = Devices()
