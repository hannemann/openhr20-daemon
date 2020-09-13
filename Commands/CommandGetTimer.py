import sys


class CommandGetTimer:

    abbr = 'get_timer'
    sent = 0
    command = 'R'
    weight = 2

    def __init__(self, day, slot):
        self.command = '%s%d%d' % (self.command, day, slot)

    @staticmethod
    def valid(day, slot):
        return 0 <= day <= 7 and 0 <= slot <= 7

    def __del__(self):
        print('Command %s deleted' % self.command)
        sys.stdout.flush()
