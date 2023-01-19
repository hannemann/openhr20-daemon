import sys
import serial
import os
import time
from serial.serialutil import SerialException
from threading import Event


class SerialIO:

    ser = None
    connecting = True
    connected = Event()
    master = os.getenv("OPENHR20_MASTER")
    baud = int(os.getenv("OPENHR20_BAUD"))
    timeout = int(os.getenv("OPENHR20_TIMEOUT"))
    debug = os.getenv('OPENHR20_DEBUG') == 'true'

    def __init__(self):
        self.connect()
        self.connected.set()

    def write(self, payload, end='\n'):
        if self.debug:
            print(' > ' + payload, end=end)
            sys.stdout.flush()
        self.ser.write((payload + '\n').encode('utf_8'))

    def read(self, end='\n'):
        try:
            if not self.connecting:
                line = self.ser.readline(256).decode('utf_8').strip()
                if line != '' and line is not None and len(line) > 0:
                    if self.debug:
                        print(' < ' + line, end=end)
                        sys.stdout.flush()
                    return line
        except SerialException as error:
            print('SerialIO: {}'.format(error))
            sys.stdout.flush()
            self.shutdown()
            self.connect()

    def connect(self):
        self.connecting = True
        self.ser = None
        while self.ser is None:
            try:
                self.ser = serial.Serial(self.master, self.baud, timeout=self.timeout)
                print('SerialIO: connection initialized')
                sys.stdout.flush()
                self.connecting = False
            except SerialException as error:
                self.ser = None
                print('SerialIO: {}'.format(error))
                sys.stdout.flush()
                time.sleep(1)

    def shutdown(self):
        self.ser.close()
        print('Serial connection closed')
        sys.stdout.flush()


serialIO = SerialIO()
