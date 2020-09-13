import sys
from Eeprom import get_eeprom_layout
from Devices import devices


class CommandGetSetting:

    abbr = 'get_setting'
    sent = 0
    command = 'G'
    weight = 4

    def __init__(self, idx):
        self.command = '%s%s' % (self.command, idx.lower())

    @staticmethod
    def valid(addr, idx):
        settings = devices.get_device_settings(addr)
        if 'ff' not in settings:
            return False
        fields = get_eeprom_layout(int('0x%0.2x' % settings['ff'], 16))
        return next((x for x in fields if x['idx'] == idx), False)

    def __del__(self):
        print('Command %s deleted' % self.command)
        sys.stdout.flush()
