from Devices import devices
from bottle import template, static_file, route
from Eeprom import get_eeprom_layout


class PageController:

    def __init__(self, httpd_path):
        self.httpd_path = httpd_path
        route('/static/<filepath:path>')(self.server_static)
        route('/')(self.index)
        route('/groups')(self.groups)
        route('/settings/<addr:int>', method='GET')(self.settings)
        route('/timers/<addr:int>', method='GET')(self.timers)

    def server_static(self, filepath):
        return static_file(filepath, root=self.httpd_path + 'assets/dist')

    @staticmethod
    def index():
        groups = sorted(devices.get_groups().values(), key=lambda g: g.name)
        ungrouped = sorted([d for d in devices.get_devices(with_remote=True).values() if d.group is None], key=lambda d: d.name)

        return template('index', title='OpenHR20', ungrouped_devices=ungrouped, groups=groups)

    @staticmethod
    def groups():
        ungrouped = [d for d in devices.devices.values() if d.group is None]
        return template('groups', title='Groups', ungrouped_devices=ungrouped, groups=devices.groups.values())

    @staticmethod
    def settings(addr):
        try:
            if devices.is_remote_device(addr):
                settings = devices.get_device_from_remote(addr).settings
            else:
                settings = devices.get_device(addr).settings
            if 'ff' in settings:
                layout = get_eeprom_layout(int('0x' + settings['ff'], 16))
                return template('settings', title='Settings', layout=layout, device_settings=settings)
        except KeyError:
            pass
        print(' < HTTP: {} settings'.format(addr))

    @staticmethod
    def timers(addr):
        try:
            if devices.is_remote_device(addr):
                device = devices.get_device_from_remote(addr)
            else:
                device = devices.get_device(addr)
            mode = device.settings['22']
            mode = 1 if mode is not None and int(mode, 16) > 0 else 0
            preset0 = device.settings['01']
            preset1 = device.settings['02']
            preset2 = device.settings['03']
            preset3 = device.settings['04']
            presets = [
                {'id': 0, 'name': 'Frost', 'temp': preset0 if preset0 is not None else '00'},
                {'id': 1, 'name': 'Eco', 'temp': preset1 if preset1 is not None else '00'},
                {'id': 2, 'name': 'Comfort', 'temp': preset2 if preset2 is not None else '00'},
                {'id': 3, 'name': 'Super Comfort', 'temp': preset3 if preset3 is not None else '00'},
            ]
            return template('timers', title='Timers', mode=mode, timers=device.timers, presets=presets)
        except KeyError:
            pass
        print(' < HTTP: {} timers'.format(addr))
