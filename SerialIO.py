import sys
import serial
from serial.serialutil import SerialException
from Config import config
from threading import Event


class SerialIO:

    ser = None
    connected = Event()

    def __init__(self):
        try:
            self.ser = serial.Serial(
                config['openhr20'].get('master', '/dev/ttyUSB0'),
                config['openhr20'].get('baud', 38400),
                timeout=int(config['openhr20'].get('timeout', 1)))
            self.connected.set()
            print('Serial connection initialized')
            sys.stdout.flush()
        except SerialException:
            print('\n!**********\nSerialError: COULD NOT ESTABLISH SERIAL CONNECTION TO %s\n!**********\n' %
                  config['openhr20'].get('master', '/dev/ttyUSB0'))
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
