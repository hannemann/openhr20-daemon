#!/usr/bin/env python3

from datetime import datetime
import serial

ser = serial.Serial('/dev/ttyUSB0', 38400)


class Openhr20(object):

    def __init__(self):
        print('Initialized')

    def action(self, line):
        print(line)
        if line == b'RTC?\n':
            d = datetime.now()

            t = "H%0.2X%0.2X%0.2X%0.2x\n" % (
                d.hour, d.minute, d.second, d.microsecond)
            date = "Y%0.2X%0.2X%0.2X\n" % (
                d.year - 2000, d.month, d.day)
            print(t + ' ' + date)

            ser.write(date.encode('utf_8'))
            ser.write(t.encode('utf_8'))

    def run(self):
        print('OpenHR20 Python Daemon')
        while True:
            line = ser.readline()
            if line:
                self.action(line)


if __name__ == "__main__":
    openhr20 = Openhr20()
    openhr20.run()
