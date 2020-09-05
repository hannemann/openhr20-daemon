import sys


class CommandStatus:

    abbr = 'status'
    sent = 0
    command = 'D'
    weight = 10

    def __del__(self):
        print('Command %s deleted' % self.command)
        sys.stdout.flush()
