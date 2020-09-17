import configparser
import os
import json
from Device import Device


class Devices:

    def __init__(self):
        self.file = '/var/cache/openhr20/devices.conf'
        self.buffer = configparser.ConfigParser()
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
        for addr, device in self.devices.items():
            if device.group is not None:
                device.group['devices'] = [d for d in self.devices.values() if d.addr in [d for d in device.group['devices']]]

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

    def get_devices(self):
        devs = {}
        for addr, device in self.devices.items():
            devs[addr] = device.get_data()
        return devs

    def has_device(self, addr):
        return True if str(addr) in self.devices else False

    def get_device(self, addr):
        return self.devices[str(addr)]


devices = Devices()
