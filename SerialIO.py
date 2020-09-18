import sys
import serial
from serial.serialutil import SerialException
from Config import config, defaults
from threading import Event


class SerialIO:

    ser = None
    connected = Event()

    def __init__(self):
        try:
            self.ser = serial.Serial(
                config.get('openhr20', 'master', fallback=defaults['openhr20']['master']),
                config.getint('openhr20', 'baud', fallback=defaults['openhr20']['baud']),
                timeout=config.getint('openhr20', 'timeout', fallback=defaults['openhr20']['timeout']))
            self.connected.set()
            print('Serial connection initialized')
            sys.stdout.flush()
        except SerialException:
            print('\n!**********\nSerialError: COULD NOT ESTABLISH SERIAL CONNECTION TO %s\n!**********\n' %
                  config.get('openhr20', 'master', fallback='/dev/ttyUSB0'))
            sys.stdout.flush()

    def write(self, payload, end='\n'):
        print(' > ' + payload, end=end)
        sys.stdout.flush()
        self.ser.write((payload + '\n').encode('utf_8'))

    def read(self, end='\n'):
        line = self.ser.readline(256).decode('utf_8').strip()
        if line != '' and line is not None and len(line) > 0:
            print(' < ' + line, end=end)
            sys.stdout.flush()
            return line

    def shutdown(self):
        self.ser.close()
        print('Serial connection closed')
        sys.stdout.flush()


serialIO = SerialIO()
