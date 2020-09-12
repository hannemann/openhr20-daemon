import sys
from Commands.CommandGetSetting import CommandGetSetting
from SerialIO import serialIO
from RTC import write as write_rtc
import threading
from Commands.Commands import commands
from Stats import Stats
from Devices import devices, write_file as write_devices, get_device_settings, set_device_settings
import json


class OpenHR20 (threading.Thread):

    daemon = True
    alive = False
    addr = -1
    data = ''
    stopped = threading.Event()
    devices = {}

    def __init__(self):
        threading.Thread.__init__(self)
        self.devices = {}
        print('OpenHR20 Thread Initialized')
        sys.stdout.flush()

    def update_device_stats(self, stats):
        devices.set('stats', '%s' % self.addr, json.dumps(stats))
        write_devices()

    def update_device_setting(self, idx, value):
        settings = get_device_settings(self.addr)
        idx = int('0x' + idx, 16)
        settings[idx] = value
        set_device_settings(self.addr, settings)
        write_devices()

    def run(self):
        self.alive = True
        write_rtc()
        print('OpenHR20: Starting main loop...')
        sys.stdout.flush()
        while self.alive:
            self.action(serialIO.read(''))

        print('OpenHR20: Main loop stopped')
        sys.stdout.flush()
        self.stopped.set()

    def action(self, line):

        if line is not None and len(line) > 0:
            if len(line) >= 4 and line[0] == '(' and line[3] == ')':
                ''' decode addr '''
                self.addr = int(line[1:3], 16)
                self.data = line[4:]
                print(
                    ' %s' %
                    '(' + devices['names'][str(self.addr)] + ')' if str(self.addr) in devices['names'] else '',
                    end=''
                )
            elif line[0] == '*':
                ''' command success '''
                print('')
                commands.remove_from_buffer(self.addr)
                self.data = line[1:]
                if not commands.has_command(self.addr) and self.data[0] != ' ':
                    self.update_device_stats(Stats.create_message(self.addr, self.data))
            elif line[0] == '-':
                self.data = line[1:]
            else:
                self.data = ''
                self.addr = 0

            print('')

            if line == 'RTC?':
                write_rtc()
            elif line == 'OK' or (line[0] == 'd' and len(line) > 2 and line[2] == ' '):
                '''noop'''
            elif line == 'N0?' or line == 'N1?':
                serialIO.write(self.sync_package(line))
            else:
                if len(self.data) > 0 and self.addr > 0 and str(self.addr) in devices['names']:
                    if self.data[0] == '?':
                        if '255' not in get_device_settings(self.addr):
                            commands.add(self.addr, CommandGetSetting(255))
                        commands.send(self.addr)
                    elif line[0] != '*' and (self.data[0] == 'D' or self.data[0] == 'A') and self.data[1] == ' ':
                        self.update_device_stats(Stats.create_message(self.addr, self.data))
                    elif len(self.data) >= 5 and self.data[1] == '[' and self.data[4] == ']' and self.data[5] == '=':
                        if self.data[0] == 'G':
                            self.update_device_setting(self.data[2:4], self.data[6:])

    def sync_package(self, line):
        req = [0, 0, 0, 0]
        v = 'O0000'
        pr = 0
        if len(commands.buffer) > 0:
            for self.addr in sorted(commands.buffer, key=lambda k: len(commands.buffer[k]), reverse=True):
                v = None
                cmnds = commands.buffer[self.addr]
                if line == 'N1?' and len(cmnds) > 10:
                    v = "O%02x%02x" % (self.addr, pr)
                    pr = self.addr
                else:
                    req[int(self.addr/8)] |= int(pow(2, self.addr % 8))

        if v is None:
            v = "P%02x%02x%02x%02x" % (req[0], req[1], req[2], req[3])

        return v

    def shutdown(self):
        self.alive = False
        ''' wait for loop to be stopped '''
        self.stopped.wait(2)


openhr20 = OpenHR20()
