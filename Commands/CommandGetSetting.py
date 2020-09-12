import sys
from Eeprom import get_fields_by_layout


class CommandSetSetting:

    abbr = 'set_setting'
    sent = 0
    command = 'S'
    weight = 4

    def __init__(self, device, field, value):
        field = get_fields_by_layout(device.layout)
        self.command = '%s%2x%2x' % (self.command, field, value)

    @staticmethod
    def valid(device, field, value):
        return True

    def __del__(self):
        print('Command %s deleted' % self.command)
        sys.stdout.flush()
