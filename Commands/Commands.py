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
            print(' %s' % '(' + devices.get_name(addr) + ')' if devices.get_name(addr) is not None else '')

    def remove_from_buffer(self, addr):
        if self.has_command(addr):
            self.buffer[addr] = sorted(self.buffer[addr], key=lambda k: k.sent)
            for cmnd in self.buffer[addr]:
                if cmnd.sent > 0:
                    self.buffer[addr].remove(cmnd)
                    break

            if len(self.buffer) < 1:
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
        if devices.get_name(addr) is not None and CommandTemperature.valid(temperature):
            group = devices.get_device_group(addr)
            if group is None:
                group = [addr]
            for addr in group:
                self.add(addr, CommandTemperature(temperature))
            return True
        return False

    def set_mode(self, addr, mode):
        if devices.get_name(addr) is not None and CommandMode.valid(mode):
            group = devices.get_device_group(addr)
            if group is None:
                group = [addr]
            for addr in group:
                self.add(addr, CommandMode(mode))
            return True
        return False

    def update_stats(self, addr):
        if devices.get_name(addr) is not None:
            if devices.get_stat(addr, 'available') == devices.AVAILABLE_OFFLINE:
                devices.set_stat(addr, 'available', devices.AVAILABLE_ONLINE)
                devices.set_stat(addr, 'time', int(time.time()))
            self.add(addr, CommandStatus())
            return True
        return False

    def reboot_device(self, addr):
        if devices.get_name(addr) is not None:
            self.add(addr, CommandReboot())
            return True
        return False

    def request_settings(self, addr):
        if devices.get_name(addr) is not None:
            layout = devices.get_setting(addr, 'ff')
            if layout is not None:
                devices.reset_device_settings(addr)
                for field in get_eeprom_layout(int('0x' + layout, 16)):
                    self.add(addr, CommandGetSetting(field['idx']))
                return True
        return False

    def set_setting(self, addr, idx, value):
        settings = devices.get_device_settings(addr)
        if devices.get_name(addr) is not None and CommandSetSetting.valid(settings['ff'], idx, value):
            self.add(addr, CommandSetSetting(idx, value))
            return True
        return False

    def request_timers(self, addr):
        if devices.get_name(addr) is not None:
            self.add(addr, CommandGetSetting('22'))
            for day in range(8):
                for slot in range(8):
                    self.add(addr, CommandGetTimer(day, slot))
            return True
        return False

    def set_timer(self, addr, day, value):
        if devices.get_name(addr) is not None and CommandSetTimer.valid(day, value):
            self.add(addr, CommandSetTimer(day, value))
            return True
        return False


commands = Commands()
