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
            for addr in self.buffer['names']:
                self.set_stat(addr, 'time', int(time.time()))
                self.set_availability(addr)
                dev = Device(addr)
                dev.set_stats(self.get_device_stats(addr))
                dev.timers = self.get_device_timers(addr)
                dev.settings = self.get_device_settings(addr)
                dev.group = self.get_device_group(addr)
                dev.name = self.buffer.get('names', addr)
                self.devices[addr] = dev

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

    def get_device_settings(self, addr):
        return json.loads(self.buffer.get('settings', str(addr), fallback='{}'))

    def set_device_settings(self, addr, settings):
        self.buffer.set('settings', str(addr), json.dumps(settings))
        try:
            self.get_device(addr).settings = settings
        except KeyError:
            pass

    def get_device_stats(self, addr):
        return json.loads(self.buffer.get('stats', str(addr), fallback='{"addr":%s}' % addr))

    def set_device_stats(self, addr, stats):
        self.buffer.set('stats', str(addr), json.dumps(stats))
        self.last_sync[str(addr)] = time.time()
        try:
            self.get_device(addr).set_stats(stats)
        except KeyError:
            pass

    def get_device_timers(self, addr):
        return json.loads(self.buffer.get('timers', str(addr), fallback=json.dumps(self.initialTimers)))

    def get_device_group(self, addr):
        for name in self.buffer['groups']:
            group = self.get_group(name)
            if int(addr) in group:
                return group
        return None

    def set_device_timers(self, addr, timers):
        self.buffer.set('timers', str(addr), json.dumps(timers))
        try:
            self.get_device(addr).timers = timers
        except KeyError:
            pass

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
            device = self.get_device(addr)
            devs[int(addr)] = {
                'name': device.name,
                'stats': device.get_stats(),
                'timers': device.timers,
                'settings': device.settings,
                'group': device.group,
            }
        return devs

    def has_device(self, addr):
        return True if str(addr) in self.devices else False

    def get_device(self, addr):
        return self.devices[str(addr)]


devices = Devices()
