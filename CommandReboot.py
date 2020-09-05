import sys


class CommandReboot:

    abbr = 'reboot'
    sent = 0
    command = 'B1324'
    weight = 10

    def __del__(self):
        print('Command %s deleted' % self.command)
        sys.stdout.flush()
