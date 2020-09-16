import json
import time


class Device:

    AVAILABLE_WARN = 'warn'
    AVAILABLE_ONLINE = 'online'
    AVAILABLE_OFFLINE = 'offline'

    mode = '-'
    valve = 0
    real = 0
    time = 0
    synced = False
    available = AVAILABLE_ONLINE
    wanted = 0
    battery = 0
    error = 0

    def __init__(self, addr, name, stats, timers, settings, group):
        self.addr = addr
        self.name = name
        self.set_stats(stats)
        self.timers = timers
        self.settings = settings
        self.group = group

    def __str__(self):
        return json.dumps(self.get_stats())

    def __index__(self):
        return self.addr

    def get_data(self):
        return {
            "name": self.name,
            "stats": self.get_stats(),
            "timers": self.timers,
            "settings": self.settings,
            "group": self.group
        }

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

    def set_stats(self, stats):
        for key, value in stats.items():
            setattr(self, key, value)
        self.set_availability()
        return self

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
