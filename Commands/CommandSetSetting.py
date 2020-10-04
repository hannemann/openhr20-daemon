from Commands.AbstractCommand import AbstractCommand
from Eeprom import get_eeprom_layout


class CommandSetSetting(AbstractCommand):

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
