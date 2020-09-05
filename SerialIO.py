import sys

import serial
from Config import config


class SerialIO:

    ser = None

    def __init__(self):
        self.ser = serial.Serial(
            config['openhr20'].get('master', '/dev/ttyUSB0'),
            config['openhr20'].get('baud', 38400),
            timeout=int(config['openhr20'].get('timeout', 1)))
        print('Serial connection initialized')
        sys.stdout.flush()

    def write(self, payload):
        print(' > ' + payload)
        sys.stdout.flush()
        self.ser.write((payload + '\n').encode('utf_8'))

    def read(self):
        line = self.ser.readline(256).decode('utf_8').strip()
        if line != '' and line is not None and len(line) > 0:
            print(' < ' + line)
            sys.stdout.flush()
            return line

    def shutdown(self):
        self.ser.close()
        print('Serial connection closed')
        sys.stdout.flush()


serialIO = SerialIO()
