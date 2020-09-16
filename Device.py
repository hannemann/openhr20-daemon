import json
import time


class Device:

    AVAILABLE_WARN = 'warn'
    AVAILABLE_ONLINE = 'online'
    AVAILABLE_OFFLINE = 'offline'

    def __init__(self, addr):
        self.addr = addr
        self.name = ''
        self.timer = None
        self.settings = None
        self.group = ''
        self.mode = '-'
        self.valve = 0
        self.real = 0
        self.wanted = 0
        self.battery = 0
        self.error = 0
        self.time = 0
        self.synced = True
        self.available = Device.AVAILABLE_ONLINE
        self.timers = {}
        self.settings = {}
        self.group = []
        self.group_name = ''

    def __str__(self):
        return json.dumps(self.get_stats())

    def __index__(self):
        return self.addr

    def set_stats(self, stats):
        for key, value in stats.items():
            setattr(self, key, value)
        self.set_availability()
        return self

    def get_stats(self):
        return {
            "addr": self.addr,
            "mode": self.mode,
            "valve": self.valve,
            "real": self.real,
            "wanted": self.wanted,
            "battery": self.battery,
            "error": self.error,
            "time": self.time,
            "synced": self.synced,
            "available": self.available
        }

    def set_availability(self):
        time_diff = int(time.time()) - self.time
        if time_diff >= 60 * 10:
            self.available = self.AVAILABLE_OFFLINE
            self.synced = True
        elif time_diff >= 60 * 5:
            self.available = self.AVAILABLE_WARN
        else:
            self.available = self.AVAILABLE_ONLINE

    def is_available(self):
        return self.available != Device.AVAILABLE_OFFLINE

    def set_setting(self, key, value):
        self.settings[key] = value
        self.set_availability()

    def set_timer(self, day, slot, minute):
        self.timers[day][slot] = minute
        self.set_availability()

    def reset_settings(self):
        self.settings = {'ff': self.settings['ff']}
