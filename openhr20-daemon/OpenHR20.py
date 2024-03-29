import sys
import os
from RTC import write as write_rtc
import threading
from Commands.Commands import commands
from Stats import Stats
import __init__ as daemon


class OpenHR20 (threading.Thread):

    daemon = True
    alive = False
    addr = -1
    data = ''
    stopped = threading.Event()
    device = None
    debug = os.getenv('OPENHR20_DEBUG') == 'true'

    def __init__(self):
        threading.Thread.__init__(self)
        print('OpenHR20 Thread Initialized')
        if self.debug:
            print('OpenHR20 Debug enabled')
        sys.stdout.flush()

    def run(self):
        self.alive = True
        write_rtc()
        print('OpenHR20: Starting main loop...')
        sys.stdout.flush()
        while self.alive:
            self.action(daemon.serialIO.read(''))

        print('OpenHR20: Main loop stopped')
        sys.stdout.flush()
        self.stopped.set()

    def action(self, line):

        if line is not None and len(line) > 0:
            if len(line) >= 4 and line[0] == '(' and line[3] == ')':
                ''' decode addr '''
                self.parse_device_line(line)
            elif line[0] == '*':
                ''' command success '''
                self.data = line[1:]
                self.handle_success(line)
            elif line[0] == '-':
                self.data = line[1:]
            else:
                self.data = ''
                self.device = None

            if self.debug:
                print('')

            if line == 'RTC?':
                write_rtc()
            elif line == 'OK' or (line[0] == 'd' and len(line) > 2 and line[2] == ' '):
                '''noop'''
            elif line == 'N0?' or line == 'N1?':
                self.handle_n_line(line)
            elif len(self.data) > 0 and self.device is not None:
                self.handle_data(line)

    def parse_device_line(self, line):
        try:
            self.device = daemon.devices.get_device(int(line[1:3], 16))
            self.data = line[4:]
            if self.debug:
                print(' ({})'.format(self.device.name) if self.device is not None else '', end='')
            self.device.set_availability()
            if not self.device.is_available():
                commands.discard_all(self.device)
        except KeyError:
            pass

    def handle_success(self, line):
        if self.debug:
            print('')
        if line[2] != '!' and line[1] != ' ':
            pending = commands.remove_from_buffer(self.device)
            if pending == 0 and self.data[0] in ['A', 'M', 'D']:
                self.update_device_stats(Stats.create(self.device, self.data))
            else:
                if pending == 0:
                    daemon.mqtt.publish_stats(self.device)
                daemon.ws.send_device_stats(self.device)


    @staticmethod
    def handle_n_line(line):
        daemon.devices.flush()
        commands.send_sync_package(line)
        for device in daemon.devices.devices.values():
            daemon.mqtt.publish_stats(device)
            daemon.mqtt.publish_availability(device)
            daemon.ws.send_device_stats(device)

    def handle_data(self, line):
        if self.data[0] == '?' and self.device.is_available():
            self.device.request_missing_timers()
            self.device.request_missing_settings()
            commands.send(self.device)
        elif line[0] != '*' and (self.data[0] == 'D' or self.data[0] == 'A') and self.data[1] == ' ':
            self.update_device_stats(Stats.create(self.device, self.data))
        elif len(self.data) >= 5 and self.data[1] == '[' and self.data[4] == ']' and self.data[5] == '=':
            if self.data[0] in ['G', 'S']:
                self.device.set_setting(self.data[2:4], self.data[6:])
            if self.data[0] in ['R', 'W']:
                self.device.set_timer(int(self.data[2:3]), int(self.data[3:4]), self.data[6:])

    def update_device_stats(self, stats):
        self.device.set_stats(stats)
        daemon.mqtt.publish_stats(self.device)
        daemon.mqtt.publish_availability(self.device)
        daemon.ws.send_device_stats(self.device)

    def shutdown(self):
        self.alive = False
        ''' wait for loop to be stopped '''
        self.stopped.wait(2)
