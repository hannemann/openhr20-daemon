import sys


class CommandTemperature:

    abbr = 'temp'
    sent = 0
    command = ''
    weight = 10

    def __init__(self, temperature):
        self.command = 'A%02x' % int(float(temperature)*2)

    @staticmethod
    def valid(temperature):
        return 5 <= float(temperature) <= 30

    def __del__(self):
        print('Command %s deleted' % self.command)
        sys.stdout.flush()
