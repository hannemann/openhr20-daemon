import serial


class SerialIO:

    ser = None

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyUSB0', 38400, timeout=1)
        print('Serial connection initialized')

    def write(self, payload):
        print(' > ' + payload)
        self.ser.write((payload + '\n').encode('utf_8'))

    def read(self):
        line = self.ser.readline(256).decode('utf_8').strip()
        if line != '' and line is not None and len(line) > 0:
            print(' < ' + line)
            return line

    def shutdown(self):
        self.ser.close()


serialIO = SerialIO()
