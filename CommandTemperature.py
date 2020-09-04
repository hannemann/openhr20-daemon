from SerialIO import serialIO


class CommandTemperature:

    sent = 0
    command = ''
    weight = 10

    def __init__(self, temperature):
        self.command = 'A%0.2x' % (temperature*2)

    def __del__(self):
        print('Command %s deleted' % self.command)
