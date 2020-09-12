import configparser
import os
import json


class Devices:

    def __init__(self):
        self.file = '/var/cache/openhr20/devices.conf'
        self.buffer = configparser.ConfigParser()

        if not os.path.exists(self.file):
            self.buffer['names'] = {
                '10': 'Livingroom',
                '11': 'Bathroom'
            }
            self.buffer['stats'] = {}
            self.buffer['timer'] = {}
            self.buffer['settings'] = {}

            self.flush()
        else:
            self.read()

    def flush(self):
        fd = open(self.file, 'w')
        self.buffer.write(fd)
        fd.close()

    def read(self):
        self.buffer.read(self.file)

    def get_name(self, addr):
        return self.buffer.get('names', str(addr), fallback=None)

    def get_device_settings(self, addr):
        return json.loads(self.buffer.get('settings', str(addr), fallback='{}'))

    def set_device_settings(self, addr, settings):
        self.buffer.set('settings', str(addr), json.dumps(settings))

    def get_device_stats(self, addr):
        return json.loads(self.buffer.get('stats', str(addr), fallback='{}'))

    def set_device_stats(self, addr, settings):
        self.buffer.set('stats', str(addr), json.dumps(settings))

    def get_stat(self, addr, stat):
        if str(addr) in self.buffer['stats'] and stat in self.buffer['stats'][str(addr)]:
            return self.get_device_stats(addr)[stat]
        return None

    def set_stat(self, addr, stat, value):
        if str(addr) in self.buffer['stats']:
            stats = self.get_device_stats(addr)
            stats[stat] = value
            self.set_device_stats(addr, stats)

    def get_devices_dict(self):
        devs = {}
        for addr in self.buffer['names']:
            devs[int(addr)] = {
                'name': self.buffer.get('names', addr),
                'stats': json.loads(self.buffer.get('stats', addr, fallback='{}')),
                'timer': json.loads(self.buffer.get('timer', addr, fallback='{}')),
                'settings': self.get_device_settings(addr),
            }
        return devs


devices = Devices()
