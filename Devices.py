import configparser
import os
import json
import time


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
            for addr in self.buffer['names']:
                self.set_stat(addr, 'time', int(time.time()))
                self.set_availability(addr)

        self.flush()

    def flush(self):
        fd = open(self.file, 'w')
        self.buffer.write(fd)
        fd.close()
        print('Flushed devices to %s' % self.file)

    def read(self):
        self.buffer.read(self.file)
        for addr in self.buffer['names']:
            self.set_device_stats(addr, self.get_device_stats(addr))
            self.set_device_settings(addr, self.get_device_settings(addr))
            self.set_device_timers(addr, self.get_device_timers(addr))

        for name in self.buffer['groups']:
            self.set_group(name, self.get_group(name))

    def get_group(self, name):
        return json.loads(self.buffer.get('groups', name, fallback=[]))

    def set_group(self, name, group):
        return self.buffer.set('groups', name, json.dumps(group))

    def get_name(self, addr):
        return self.buffer.get('names', str(addr), fallback=None)

    def get_device_settings(self, addr):
        return json.loads(self.buffer.get('settings', str(addr), fallback='{}'))

    def set_device_settings(self, addr, settings):
        self.buffer.set('settings', str(addr), json.dumps(settings))

    def get_device_stats(self, addr):
        return json.loads(self.buffer.get('stats', str(addr), fallback='{"addr":%s}' % addr))

    def set_device_stats(self, addr, settings):
        self.buffer.set('stats', str(addr), json.dumps(settings))
        self.last_sync[str(addr)] = time.time()

    def get_device_timers(self, addr):
        return json.loads(self.buffer.get('timers', str(addr), fallback=json.dumps(self.initialTimers)))

    def get_device_group(self, addr):
        for name in self.buffer['groups']:
            group = self.get_group(name)
            if addr in group:
                return group
        return None

    def set_device_timers(self, addr, settings):
        self.buffer.set('timers', str(addr), json.dumps(settings))
        self.last_sync[str(addr)] = time.time()

    def get_stat(self, addr, stat):
        if str(addr) in self.buffer['stats'] and stat in self.buffer['stats'][str(addr)]:
            return self.get_device_stats(addr)[stat]
        return None

    def set_stat(self, addr, stat, value):
        if str(addr) in self.buffer['stats']:
            stats = self.get_device_stats(addr)
            stats[stat] = value
            self.set_device_stats(addr, stats)

    def get_setting(self, addr, setting):
        if str(addr) in self.buffer['settings'] and setting in self.buffer['settings'][str(addr)]:
            return self.get_device_settings(addr)[setting]
        return None

    def set_setting(self, addr, setting, value):
        if str(addr) in self.buffer['settings']:
            settings = self.get_device_settings(addr)
            settings[setting] = value
            self.set_device_settings(addr, settings)

    def set_timer(self, addr, day, slot, minute):
        if str(addr) in self.buffer['timers']:
            timers = self.get_device_timers(addr)
            timers[day][slot] = minute
            self.set_device_timers(addr, timers)

    def reset_device_settings(self, addr):
        self.set_device_settings(addr, {'ff': self.get_setting(addr, 'ff')})

    def set_availability(self, addr):
        time_diff = int(time.time()) - self.get_stat(addr, 'time')
        if time_diff >= 60 * 10:
            self.set_stat(addr, 'available',  self.AVAILABLE_OFFLINE)
            self.set_stat(addr, 'synced',  True)
        elif time_diff >= 60 * 5:
            self.set_stat(addr, 'available',  self.AVAILABLE_WARN)
        else:
            self.set_stat(addr, 'available',  self.AVAILABLE_ONLINE)

    def get_devices_dict(self):
        devs = {}
        for addr in self.buffer['names']:
            devs[int(addr)] = {
                'name': self.get_name(addr),
                'stats': self.get_device_stats(addr),
                'timers': self.get_device_timers(addr),
                'settings': self.get_device_settings(addr),
            }
        return devs


devices = Devices()
