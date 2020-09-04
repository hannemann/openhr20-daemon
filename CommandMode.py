from SerialIO import serialIO


class CommandMode:

    sent = 0
    command = 'M00'
    weight = 10
    modes = {
        'MANU': 'M%0.2x' % 0,
        'AUTO': 'M%0.2x' % 1,
    }

    def __init__(self, mode):
        self.command = self.modes[mode]
