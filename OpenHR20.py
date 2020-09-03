from datetime import datetime
import serial
import threading
from Commands import commands

ser = serial.Serial('/dev/ttyUSB0', 38400)


class OpenHR20 (threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        print('Initialized')

    def action(self, line):

        print(' < ' + line)

        if len(line) >= 4 and line[0] == '(' and line[3] == ')':
            addr = int(line[1:3], 16)
            #print("Addr: {}".format(addr))
        else:
            addr = 0

        if line == 'RTC?':
            self.writeRTC()
        elif line == 'OK' or line[0] == 'd' or len(line) > 2 and line[2] == ' ':
            '''noop'''
        elif line == 'N0?' or line == 'N1?':
            v = 'O0000'
            if False: # having commands...
                req = [0, 0, 0, 0]
                pr = 0

            print(' > ' + v)
            ser.write((v + '\n').encode('utf_8'))

    def run(self):
        print('OpenHR20 Python Daemon\n')
        print('Starting...\n')
        self.writeRTC()
        while True:
            line = ser.readline().decode('utf_8').strip()
            if line != '':
                self.action(line)

    def writeRTC(self):
        """
        H160b0004
        Y140902

        H16122842 Y140902
        :return:
        """

        d = datetime.now()
        t = "H%0.2X%0.2X%0.2X%0.2X" % (
            d.hour, d.minute, d.second, round(d.microsecond / 10000))
        date = "Y%0.2X%0.2X%0.2X" % (
            d.year - 2000, d.month, d.day)
        print(' > ' + t + ' ' + date)
        ser.write((date + '\n').encode('utf_8'))
        ser.write((t + '\n').encode('utf_8'))