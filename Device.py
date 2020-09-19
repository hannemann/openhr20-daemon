import json
import time
from Commands.CommandTemperature import CommandTemperature
from Commands.CommandMode import CommandMode
from Commands.CommandStatus import CommandStatus
from Commands.CommandGetSetting import CommandGetSetting
from Commands.CommandSetSetting import CommandSetSetting
from Commands.CommandReboot import CommandReboot
from Commands.CommandGetTimer import CommandGetTimer
from Commands.CommandSetTimer import CommandSetTimer
from Eeprom import get_eeprom_layout
from Commands.Commands import commands
from Group import Group


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
    group = None

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

        group = None
        if self.group is not None:
            group_addrs = [device.addr for device in self.group.devices]
            group = {
                'name': self.group.name,
                'devices': group_addrs
            }

        return {
            "name": self.name,
            "stats": self.get_stats(),
            "timers": self.timers,
            "settings": self.settings,
            "group": group
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
            "available": self.available,
            "pending-commands": len(commands.buffer[self.addr]) if self.addr in commands.buffer else 0,
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

    def set_temperature(self, temperature):
        CommandTemperature.validate(temperature)
        group = self.group
        if group is None:
            group = Group('fake', [self])
        for device in group.devices:
            commands.add(device, CommandTemperature(temperature))

    def set_mode(self, mode):
        CommandMode.validate(mode)
        group = self.group
        if group is None:
            group = Group('fake', [self])
        for device in group.devices:
            commands.add(device, CommandMode(mode))

    def update_stats(self):
        if self.available == self.AVAILABLE_OFFLINE:
            self.available = self.AVAILABLE_ONLINE
            self.time = int(time.time())
        commands.add(self, CommandStatus())

    def reboot_device(self):
        commands.add(self, CommandReboot())

    def request_settings(self):
        try:
            layout = self.settings['ff']
            if layout is not None:
                self.reset_settings()
                for field in get_eeprom_layout(int('0x' + layout, 16)):
                    commands.add(self, CommandGetSetting(field['idx']))
        except KeyError:
            ''' no setting ff in device.settings '''
            pass

    def send_setting(self, idx, value):
        settings = self.settings
        if CommandSetSetting.valid(settings['ff'], idx, value):
            commands.add(self, CommandSetSetting(idx, value))

    def request_timers(self):
        commands.add(self, CommandGetSetting('22'))
        for day in range(8):
            for slot in range(8):
                commands.add(self, CommandGetTimer(day, slot))

    def send_timer(self, day, value):
        if CommandSetTimer.valid(day, value):
            commands.add(self, CommandSetTimer(day, value))

    def request_missing_timers(self):
        for d, day in enumerate(self.timers):
            for s, slot in enumerate(day):
                if slot == '':
                    commands.add(self, CommandGetTimer(d, s))

    def request_missing_settings(self):
        try:
            layout = self.settings['ff']
            if layout is not None:
                for field in get_eeprom_layout(int('0x' + layout, 16)):
                    if not field['idx'] in self.settings or self.settings[field['idx']] == '':
                        commands.add(self, CommandGetSetting(field['idx']))
        except KeyError:
            commands.add(self, CommandGetSetting('ff'))

