import sys
import serial
import os
from serial.serialutil import SerialException
from threading import Event


class SerialIO:

    ser = None
    connected = Event()
    master = os.getenv("OPENHR20_MASTER")
    baud = int(os.getenv("OPENHR20_BAUD"))
    timeout = int(os.getenv("OPENHR20_TIMEOUT"))

    def __init__(self):
        try:
            self.ser = serial.Serial(self.master, self.baud, timeout=self.timeout)
            self.connected.set()
            print('Serial connection initialized')
            sys.stdout.flush()
        except SerialException:
            print('\n!**********\nSerialError: COULD NOT ESTABLISH SERIAL CONNECTION TO %s\n!**********\n' %
                  self.master)
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
