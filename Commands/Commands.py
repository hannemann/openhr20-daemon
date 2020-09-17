import sys
from SerialIO import serialIO
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


class Commands:

    buffer = {}

    def add(self, device, command):
        addr = device.addr
        if addr not in self.buffer:
            self.buffer[addr] = []

        buffered_command = next((x for x in self.buffer[addr] if x.command == command.command), None)
        if buffered_command is not None:
            print('Command %s already buffered. Discarding new command...' % buffered_command.command)
            sys.stdout.flush()
        else:
            self.buffer[addr].append(command)

        device.synced = False

    def send(self, device):
        weight = 0
        bank = 0
        q = []
        i = 0
        if self.has_command(device):
            for cmnd in self.buffer[device.addr]:
                cw = cmnd.weight
                weight += cw
                if weight > 10:
                    if ++bank > 7:
                        break
                    weight = cw
                r = "(%02x-%x)%s" % (device.addr, bank, cmnd.command)
                q.append(r)
                cmnd.sent += 1
                i += 1
                if i > 25:
                    break
            serialIO.write('\n'.join(q), '')
            print(' %s' % '(' + device.name + ')')

    def remove_from_buffer(self, device):
        if self.has_command(device):
            self.buffer[device.addr] = sorted(self.buffer[device.addr], key=lambda k: k.sent)
            for cmnd in self.buffer[device.addr]:
                if cmnd.sent > 0:
                    self.buffer[device.addr].remove(cmnd)
                    break

            if len(self.buffer[device.addr]) < 1:
                del self.buffer[device.addr]

    def discard_all(self, device):
        if self.has_command(device):
            del self.buffer[device.addr]

    def has_command(self, device):
        result = device.addr in self.buffer and len(self.buffer[device.addr]) > 0
        device.synced = not result
        return result

    def set_temperature(self, device, temperature):
        CommandTemperature.validate(temperature)
        group = device.group
        if group is None:
            group = {"devices": [device]}
        for device in group['devices']:
            self.add(device, CommandTemperature(temperature))

    def set_mode(self, device, mode):
        CommandMode.validate(mode)
        group = device.group
        if group is None:
            group = {"devices": [device]}
        for device in group['devices']:
            self.add(device, CommandMode(mode))

    def update_stats(self, device):
        if device.available == device.AVAILABLE_OFFLINE:
            device.available = device.AVAILABLE_ONLINE
            device.time = int(time.time())
        self.add(device, CommandStatus())

    def reboot_device(self, device):
        self.add(device.addr, CommandReboot())

    def request_settings(self, device):
        try:
            layout = device.settings['ff']
            if layout is not None:
                device.reset_settings()
                for field in get_eeprom_layout(int('0x' + layout, 16)):
                    self.add(device, CommandGetSetting(field['idx']))
        except KeyError:
            ''' no setting ff in device.settings '''
            pass

    def set_setting(self, device, idx, value):
        settings = device.settings
        if CommandSetSetting.valid(settings['ff'], idx, value):
            self.add(device, CommandSetSetting(idx, value))

    def request_timers(self, device):
        self.add(device.addr, CommandGetSetting('22'))
        for day in range(8):
            for slot in range(8):
                self.add(device, CommandGetTimer(day, slot))

    def set_timer(self, device, day, value):
        if CommandSetTimer.valid(day, value):
            self.add(device, CommandSetTimer(day, value))


commands = Commands()
