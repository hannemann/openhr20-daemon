from Commands.AbstractCommand import AbstractCommand


class CommandMode(AbstractCommand):

    abbr = 'mode'
    sent = 0
    command = ''
    weight = 10
    modes = {
        'manu': 'M00',
        'auto': 'M01',
    }

    def __init__(self, mode):
        self.command = self.modes[mode.lower()]

    @staticmethod
    def validate(mode):
        if not mode.lower() in CommandMode.modes:
            raise ValueError
