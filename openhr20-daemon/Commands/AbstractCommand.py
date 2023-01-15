import sys


class AbstractCommand:

    command = ''

    def __del__(self):
        print(' ! Command {} deleted'.format(self.command))
        sys.stdout.flush()
