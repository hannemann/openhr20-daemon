from bottle import ServerAdapter, route, template, static_file, request, response
import bottle
import sys
from Commands.Commands import commands
import pathlib
from Config import config
from Devices import devices
import threading
import json
from Eeprom import get_eeprom_layout

debug = config.getboolean('openhr20', 'debug')
httpd_path = '/' + str(pathlib.Path(__file__).parent.absolute()).strip('/') + '/httpd/'
bottle.TEMPLATE_PATH.insert(0, httpd_path + 'views')
bottle.debug(debug)


class MyWSGIRefServer(ServerAdapter):
    """
    for shutting down cleanly
    https://stackoverflow.com/a/16056443
    """
    server = None

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler
        self.server = make_server('0.0.0.0', self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        # self.server.server_close() <--- alternative but causes bad fd exception
        self.server.shutdown()


class Httpd(threading.Thread):

    server = None

    def run(self):
        host = config.get('httpd', 'host', fallback='0.0.0.0')
        port = config.getint('httpd', 'port', fallback=8020)
        self.server = MyWSGIRefServer(port=port, host=host)
        bottle.run(server=self.server, reloader=False)
        print('HTTP Server stopped...')
        sys.stdout.flush()

    def server_static(self, filepath):
        return static_file(filepath, root=httpd_path + 'assets/dist')

    def index(self):
        return template('index', title='OpenHR20', devices=devices.get_devices_dict())

    def set_temp(self, addr):
        temp = float(request.json.get('temp'))
        commands.set_temperature(addr, temp)
        print('HTTP: %d temp %f' % (addr, temp))

    def set_mode(self, addr):
        mode = request.json.get('mode')
        commands.set_mode(addr, mode)
        print('HTTP: %d mode %s' % (addr, mode))

    def update_stats(self, addr):
        commands.update_stats(addr)
        print('HTTP: %d update_stats' % addr)

    def request_settings(self, addr):
        commands.request_settings(addr)
        print('HTTP: %d request_settings' % addr)

    def settings(self, addr):
        if devices.get_name(addr) is not None:
            settings = devices.get_device_settings(addr)
            if 'ff' in settings:
                layout = get_eeprom_layout(int('0x' + settings['ff'], 16))
                return template('settings', title='Settings', layout=layout, device_settings=settings)
        print('HTTP: %d settings' % addr)

    def set_settings(self, addr):
        if devices.get_name(addr) is not None:
            settings = devices.get_device_settings(addr)
            for idx, value in settings.items():
                new = request.json.get(idx)
                if new != value:
                    commands.set_setting(addr, idx, new)
        print('HTTP: %d set_settings' % addr)

    def request_timers(self, addr):
        commands.request_timers(addr)
        print('HTTP: %d request_timers' % addr)

    def timers(self, addr):
        if devices.get_name(addr) is not None:
            timers = devices.get_device_timers(addr)
            mode = devices.get_setting(addr, '01')
            mode = 1 if mode is not None and int(mode, 16) > 0 else 0
            preset0 = devices.get_setting(addr, '01')
            preset1 = devices.get_setting(addr, '02')
            preset2 = devices.get_setting(addr, '03')
            preset3 = devices.get_setting(addr, '04')
            presets = [
                {'id': 0, 'name': 'Frost', 'temp': preset0 if preset0 is not None else '00'},
                {'id': 1, 'name': 'Eco', 'temp': preset1 if preset1 is not None else '00'},
                {'id': 2, 'name': 'Comfort', 'temp': preset2 if preset2 is not None else '00'},
                {'id': 3, 'name': 'Super Comfort', 'temp': preset3 if preset3 is not None else '00'},
            ]
            return template('timers', title='Timers', mode=mode, timers=timers, presets=presets)
        print('HTTP: %d timers' % addr)

    def set_timers(self, addr):
        if devices.get_name(addr) is not None:
            timers = devices.get_device_timers(addr)
            for day, value in request.json.items():
                if timers[int(day[0])][int(day[1])] != value:
                    commands.set_timer(addr, day, value)
        print('HTTP: %d set_timers' % addr)

    def reboot(self, addr):
        commands.reboot_device(addr)
        print('HTTP: %d reboot' % addr)

    def get_stats(self):
        response.content_type = 'application/json'
        return json.dumps(devices.get_devices_dict())

    def shutdown(self):
        self.server.stop()


httpd = Httpd()
route('/static/<filepath:path>')(httpd.server_static)
route('/')(httpd.index)
route('/stats', method='GET')(httpd.get_stats)
route('/temp/<addr:int>', method='POST')(httpd.set_temp)
route('/mode/<addr:int>', method='POST')(httpd.set_mode)
route('/update/<addr:int>', method='POST')(httpd.update_stats)
route('/request_settings/<addr:int>', method='POST')(httpd.request_settings)
route('/settings/<addr:int>', method='GET')(httpd.settings)
route('/settings/<addr:int>', method='POST')(httpd.set_settings)
route('/request_timers/<addr:int>', method='POST')(httpd.request_timers)
route('/timers/<addr:int>', method='GET')(httpd.timers)
route('/set_timers/<addr:int>', method='POST')(httpd.set_timers)
route('/reboot/<addr:int>', method='POST')(httpd.reboot)
