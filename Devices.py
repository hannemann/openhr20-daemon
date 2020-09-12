import configparser
import os
import json
import time


class Devices:

    AVAILABLE_WARN = 'warn'
    AVAILABLE_ONLINE = 'online'
    AVAILABLE_OFFLINE = 'offline'

    def __init__(self):
        self.file = '/var/cache/openhr20/devices.conf'
        self.buffer = configparser.ConfigParser()
        self.last_sync = {}

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
            for addr in self.buffer['names']:
                self.set_stat(addr, 'time', int(time.time()))
                self.set_availability(addr)

    def flush(self):
        fd = open(self.file, 'w')
        self.buffer.write(fd)
        fd.close()

    def read(self):
        self.buffer.read(self.file)
        for addr in self.buffer['names']:
            self.set_device_stats(addr, self.get_device_stats(addr))
            self.set_device_settings(addr, self.get_device_settings(addr))
            self.set_device_timer(addr, self.get_device_timer(addr))

    def get_name(self, addr):
        return self.buffer.get('names', str(addr), fallback=None)

    def get_device_settings(self, addr):
        return json.loads(self.buffer.get('settings', str(addr), fallback='{}'))

    def set_device_settings(self, addr, settings):
        self.buffer.set('settings', str(addr), json.dumps(settings))
        self.flush()

    def get_device_stats(self, addr):
        return json.loads(self.buffer.get('stats', str(addr), fallback='{"addr":%s}' % addr))

    def set_device_stats(self, addr, settings):
        self.buffer.set('stats', str(addr), json.dumps(settings))
        self.last_sync[str(addr)] = time.time()
        self.flush()

    def get_device_timer(self, addr):
        return json.loads(self.buffer.get('timer', str(addr), fallback='{}'))

    def set_device_timer(self, addr, settings):
        self.buffer.set('timer', str(addr), json.dumps(settings))
        self.last_sync[str(addr)] = time.time()
        self.flush()

    def get_stat(self, addr, stat):
        if str(addr) in self.buffer['stats'] and stat in self.buffer['stats'][str(addr)]:
            return self.get_device_stats(addr)[stat]
        return None

    def set_stat(self, addr, stat, value):
        if str(addr) in self.buffer['stats']:
            stats = self.get_device_stats(addr)
            stats[stat] = value
            self.set_device_stats(addr, stats)

    def set_setting(self, addr, setting, value):
        if str(addr) in self.buffer['settings']:
            settings = self.get_device_settings(addr)
            settings[setting] = value
            self.set_device_settings(addr, settings)

    def set_availability(self, addr):
        time_diff = int(time.time()) - self.get_stat(addr, 'time')
        if time_diff >= 60 * 10:
            self.set_stat(addr, 'available',  self.AVAILABLE_OFFLINE)
            self.set_stat(addr, 'synced',  True)
        elif time_diff >= 60 * 5:
            self.set_stat(addr, 'available',  self.AVAILABLE_WARN)
        else:
            self.set_stat(addr, 'available',  self.AVAILABLE_ONLINE)
        self.flush()

    def get_devices_dict(self):
        devs = {}
        for addr in self.buffer['names']:
            devs[int(addr)] = {
                'name': self.get_name(addr),
                'stats': self.get_device_stats(addr),
                'timer': self.get_device_timer(addr),
                'settings': self.get_device_settings(addr),
            }
        return devs


devices = Devices()
