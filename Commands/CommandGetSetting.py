import sys
from Eeprom import get_eeprom_layout


class CommandGetSetting:

    abbr = 'get_setting'
    sent = 0
    command = 'G'
    weight = 2

    def __init__(self, idx):
        self.command = '{}{}'.format(self.command, idx.lower())

    @staticmethod
    def valid(device, idx):
        settings = device.settings
        if 'ff' not in settings:
            return False
        fields = get_eeprom_layout(int('0x' + settings['ff'], 16))
        return next((x for x in fields if x['idx'] == idx), False)

    def __del__(self):
        print('Command {} deleted'.format(self.command))
        sys.stdout.flush()
