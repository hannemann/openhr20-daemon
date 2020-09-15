import sys


class CommandMode:

    abbr = 'mode'
    sent = 0
    command = ''
    weight = 10
    modes = {
        'manu': 'M%0.2x' % 0,
        'auto': 'M%0.2x' % 1,
    }

    def __init__(self, mode):
        self.command = self.modes[mode.lower()]

    @staticmethod
    def validate(mode):
        if not mode.lower() in CommandMode.modes:
            raise ValueError

    def __del__(self):
        print('Command %s deleted' % self.command)
        sys.stdout.flush()
