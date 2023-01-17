import sys
import os


class AbstractCommand:

    command = ''

    def __del__(self):
        if os.getenv('OPENHR20_DEBUG') == 'true':
            print(' ! Command {} deleted'.format(self.command))
            sys.stdout.flush()
