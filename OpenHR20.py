import sys
from Commands.CommandGetSetting import CommandGetSetting
from MQTT import mqtt
from SerialIO import serialIO
from RTC import write as write_rtc
import threading
from Commands.Commands import commands
from Stats import Stats
from Devices import devices


class OpenHR20 (threading.Thread):

    daemon = True
    alive = False
    addr = -1
    data = ''
    stopped = threading.Event()
    device = None

    def __init__(self):
        threading.Thread.__init__(self)
        print('OpenHR20 Thread Initialized')
        sys.stdout.flush()

    def update_device_stats(self, stats):
        self.device.set_stats(stats)
        mqtt.publish_stats(self.device)

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
                try:
                    self.device = devices.get_device(int(line[1:3], 16))
                    self.data = line[4:]
                    print(
                        ' %s' %
                        '(' + self.device.name + ')' if self.device is not None else '',
                        end=''
                    )
                    self.device.set_availability()
                    if not self.device.is_available():
                        commands.discard_all(self.device)
                except KeyError:
                    pass
            elif line[0] == '*':
                ''' command success '''
                print('')
                if line[2] != '!' and line[1] != ' ':
                    commands.remove_from_buffer(self.device)
                self.data = line[1:]
                if not commands.has_command(self.device) and self.data[0] in ['A', 'M']:
                    self.update_device_stats(Stats.create(self.device, self.data))
            elif line[0] == '-':
                self.data = line[1:]
            else:
                self.data = ''
                self.device = None

            print('')

            if line == 'RTC?':
                write_rtc()
            elif line == 'OK' or (line[0] == 'd' and len(line) > 2 and line[2] == ' '):
                '''noop'''
            elif line == 'N0?' or line == 'N1?':
                devices.flush()
                commands.send_sync_package(line)
                for device in devices.devices.values():
                    mqtt.publish_stats(device)
            else:
                if len(self.data) > 0 and self.device is not None:
                    if self.data[0] == '?' and self.device.is_available():
                        if 'ff' not in self.device.settings:
                            commands.add(self.device.addr, CommandGetSetting('ff'))
                        commands.send(self.device)
                    elif line[0] != '*' and (self.data[0] == 'D' or self.data[0] == 'A') and self.data[1] == ' ':
                        self.update_device_stats(Stats.create(self.device, self.data))
                    elif len(self.data) >= 5 and self.data[1] == '[' and self.data[4] == ']' and self.data[5] == '=':
                        if self.data[0] in ['G', 'S']:
                            self.device.set_setting(self.data[2:4], self.data[6:])
                        if self.data[0] in ['R', 'W']:
                            self.device.set_timer(int(self.data[2:3]), int(self.data[3:4]), self.data[6:])

    def shutdown(self):
        self.alive = False
        ''' wait for loop to be stopped '''
        self.stopped.wait(2)


openhr20 = OpenHR20()
