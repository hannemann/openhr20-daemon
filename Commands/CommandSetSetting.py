import sys
from Eeprom import get_eeprom_layout


class CommandSetSetting:

    abbr = 'set_setting'
    sent = 0
    command = 'S'
    weight = 4

    def __init__(self, idx, value):
        self.command = '%s%s%s' % (self.command, idx, value)

    @staticmethod
    def valid(layout, idx, value):
        fields = get_eeprom_layout(layout)
        field = next((x for x in fields if x['idx'] == idx), False)
        return field and field['range'][0] <= int(value, 16) <= field['range'][1]

    def __del__(self):
        print('Command %s deleted' % self.command)
        sys.stdout.flush()
