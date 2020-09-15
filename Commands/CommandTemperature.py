import sys


class CommandTemperature:

    abbr = 'temp'
    sent = 0
    command = ''
    weight = 10

    def __init__(self, temperature):
        self.command = 'A%02x' % int(float(temperature)*2)

    @staticmethod
    def validate(temperature):
        if not 5 <= float(temperature) <= 30:
            raise ValueError

    def __del__(self):
        print('Command %s deleted' % self.command)
        sys.stdout.flush()
