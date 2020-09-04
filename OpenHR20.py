from SerialIO import serialIO
from RTC import write as writeRTC
import threading
from Commands import commands
from MQTT import mqtt


class OpenHR20 (threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        print('Initialized')

    def action(self, line):

        addr = -1

        if line is not None:
            if len(line) >= 4 and line[0] == '(' and line[3] == ')':
                addr = int(line[1:3], 16)
                data = line[4:]
            elif len(line) > 0 and line[0] == '*':
                ''' command success '''
                data = line[1:]
            else:
                data = ''
                addr = 0

            #print(' Addr %d, Data: %d - %s' % (addr, len(data), data))

            if line == 'RTC?':
                writeRTC()
            elif line == 'OK' or line[0] == 'd' or len(line) > 2 and line[2] == ' ':
                '''noop'''
            elif line == 'N0?' or line == 'N1?':
                serialIO.write(self.sync_package(line))
            else:
                if addr > 0:
                    if len(data) > 0 and data[0] == '?':
                        commands.send(addr)

    def run(self):
        print('OpenHR20 Python Daemon\n')
        print('Starting main loop...\n')
        writeRTC()
        while True:
            self.action(serialIO.read())

    @staticmethod
    def sync_package(line):
        req = [0, 0, 0, 0]
        pr = 0
        v = None
        if len(commands.buffer) > 0:
            for addr in commands.sorted_by_commands_count():
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
