from SerialIO import serialIO
from RTC import write as writeRTC
import threading
from Commands import commands


class OpenHR20 (threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        print('Initialized')

    def action(self, line):

        if line is not None:
            if len(line) >= 4 and line[0] == '(' and line[3] == ')':
                addr = int(line[1:3], 16)
                #print("Addr: {}".format(addr))
            else:
                addr = 0

            if line == 'RTC?':
                writeRTC()
            elif line == 'OK' or line[0] == 'd' or len(line) > 2 and line[2] == ' ':
                '''noop'''
            elif line == 'N0?' or line == 'N1?':
                v = 'O0000'
                if False: # having commands...
                    req = [0, 0, 0, 0]
                    pr = 0

                serialIO.write(v)

    def run(self):
        print('OpenHR20 Python Daemon\n')
        print('Starting main loop...\n')
        writeRTC()
        while True:
            self.action(serialIO.read())
