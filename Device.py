import json


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
        self.group = ''

    def __str__(self):
        return json.dumps(self.get_stats())

    def __index__(self):
        return self.addr

    def set_stats(self, stats):
        for key, value in stats.items():
            setattr(self, key, value)
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
