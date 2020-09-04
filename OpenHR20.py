from SerialIO import serialIO
from RTC import write as writeRTC
import threading
from Commands import commands
from datetime import datetime
import time


class OpenHR20 (threading.Thread):

    addr = -1
    data = ''

    def __init__(self):
        threading.Thread.__init__(self)
        print('Initialized')

    def action(self, line):

        if line is not None and len(line) > 0:
            if len(line) >= 4 and line[0] == '(' and line[3] == ')':
                ''' decode addr '''
                self.addr = int(line[1:3], 16)
                self.data = line[4:]
            elif line[0] == '*':
                ''' command success '''
                commands.remove_from_buffer(self.addr)
                self.data = line[1:]
                if not commands.has_command(self.addr):
                    print(self.data)
            elif line[0] == '-':
                self.data = line[1:]
            else:
                self.data = ''
                self.addr = 0

            if line == 'RTC?':
                writeRTC()
            elif line == 'OK' or line[0] == 'd' or len(line) > 2 and line[2] == ' ':
                '''noop'''
            elif line == 'N0?' or line == 'N1?':
                serialIO.write(self.sync_package(line))
            else:
                if self.addr > 0:
                    if len(self.data) > 0 and self.data[0] == '?':
                        commands.send(self.addr)

    def run(self):
        print('OpenHR20 Python Daemon\n')
        print('Wait for current minute to finish...')
        t = datetime.now()
        wait = 60 - (t.second + t.microsecond / 1000000.0)
        time.sleep(wait)
        print('Starting main loop...\n')
        writeRTC()
        while True:
            self.action(serialIO.read())

    def shutdown(self):
        serialIO.shutdown()

    @staticmethod
    def sync_package(line):
        req = [0, 0, 0, 0]
        pr = 0
        v = None
        if len(commands.buffer) > 0:
            for addr in sorted(commands.buffer, key=lambda k: len(commands.buffer[k]), reverse=True):
                cmnds = commands.buffer[addr]
                if line == 'N1?' and len(cmnds) > 10:
                    v = "O%02X%02X" % (addr, pr)
                    pr = addr
                else:
                    req[int(addr/8)] |= int(pow(2, addr % 8))

            if v is None:
                v = "P%02X%02X%02X%02X" % (req[0], req[1], req[2], req[3])
        else:
            v = 'O0000'

        return v
