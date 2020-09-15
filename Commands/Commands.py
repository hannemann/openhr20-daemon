import sys
from SerialIO import serialIO
from Devices import devices
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

    def add(self, addr, command):
        if addr not in self.buffer:
            self.buffer[addr] = []

        buffered_command = next((x for x in self.buffer[addr] if x.command == command.command), None)
        if buffered_command is not None:
            print('Command %s already buffered. Discarding new command...' % buffered_command.command)
            sys.stdout.flush()
        else:
            self.buffer[addr].append(command)

        devices.set_stat(addr, 'synced', False)

    def send(self, addr):
        weight = 0
        bank = 0
        q = []
        i = 0
        if self.has_command(addr):
            for cmnd in self.buffer[addr]:
                cw = cmnd.weight
                weight += cw
                if weight > 10:
                    if ++bank > 7:
                        break
                    weight = cw
                r = "(%02x-%x)%s" % (addr, bank, cmnd.command)
                q.append(r)
                cmnd.sent += 1
                i += 1
                if i > 25:
                    break
            serialIO.write('\n'.join(q), '')
            print(' %s' % '(' + devices.get_device(addr).name + ')' if devices.has_device(addr) else '')

    def remove_from_buffer(self, addr):
        if self.has_command(addr):
            self.buffer[addr] = sorted(self.buffer[addr], key=lambda k: k.sent)
            for cmnd in self.buffer[addr]:
                if cmnd.sent > 0:
                    self.buffer[addr].remove(cmnd)
                    break

            if len(self.buffer[addr]) < 1:
                del self.buffer[addr]

    def discard_all(self, addr):
        if self.has_command(addr):
            del self.buffer[addr]

    def has_command(self, addr):
        result = addr in self.buffer and len(self.buffer[addr]) > 0
        devices.set_stat(addr, 'synced', not result)
        return result

    def test(self, command):
        self.buffer[0] = command

    def set_temperature(self, addr, temperature):
        CommandTemperature.validate(temperature)
        device = devices.get_device(addr)
        group = device.group
        if group is None:
            group = [device.addr]
        for addr in group:
            self.add(devices.get_device(addr).addr, CommandTemperature(temperature))

    def set_mode(self, addr, mode):
        CommandMode.validate(mode)
        device = devices.get_device(addr)
        group = device.group
        if group is None:
            group = [addr]
        for addr in group:
            self.add(addr, CommandMode(mode))

    def update_stats(self, addr):
        device = devices.get_device(addr)
        if device.available == device.AVAILABLE_OFFLINE:
            devices.available = device.AVAILABLE_ONLINE
            devices.time = int(time.time())
        self.add(device.addr, CommandStatus())

    def reboot_device(self, addr):
        device = devices.get_device(addr)
        self.add(device.addr, CommandReboot())

    def request_settings(self, addr):
        if devices.has_device(addr):
            layout = devices.get_setting(addr, 'ff')
            if layout is not None:
                devices.reset_device_settings(addr)
                for field in get_eeprom_layout(int('0x' + layout, 16)):
                    self.add(addr, CommandGetSetting(field['idx']))
                return True
        return False

    def set_setting(self, addr, idx, value):
        settings = devices.get_device_settings(addr)
        if devices.has_device(addr) and CommandSetSetting.valid(settings['ff'], idx, value):
            self.add(addr, CommandSetSetting(idx, value))
            return True
        return False

    def request_timers(self, addr):
        if devices.has_device(addr):
            self.add(addr, CommandGetSetting('22'))
            for day in range(8):
                for slot in range(8):
                    self.add(addr, CommandGetTimer(day, slot))
            return True
        return False

    def set_timer(self, addr, day, value):
        if devices.has_device(addr) and CommandSetTimer.valid(day, value):
            self.add(addr, CommandSetTimer(day, value))
            return True
        return False


commands = Commands()
