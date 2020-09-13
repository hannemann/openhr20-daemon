import time

from bottle import ServerAdapter, route, template, static_file, request, response
import bottle
import sys
from Commands.Commands import commands
from Commands.CommandTemperature import CommandTemperature
from Commands.CommandMode import CommandMode
from Commands.CommandStatus import CommandStatus
from Commands.CommandGetSetting import CommandGetSetting
from Commands.CommandSetSetting import CommandSetSetting
from Commands.CommandReboot import CommandReboot
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

    def set_temp(self):
        addr = int(request.json.get('addr'))
        temp = float(request.json.get('temp'))
        if addr in devices.get_devices_dict() and CommandTemperature.valid(temp):
            commands.add(addr, CommandTemperature(temp))
        print('HTTP: %d temp %f' % (addr, temp))

    def set_mode(self):
        addr = int(request.json.get('addr'))
        mode = request.json.get('mode')
        if addr in devices.get_devices_dict() and CommandMode.valid(mode):
            commands.add(addr, CommandMode(mode))
        print('HTTP: %d mode %s' % (addr, mode))

    def update_stats(self):
        addr = int(request.json.get('addr'))
        message = None
        if addr in devices.get_devices_dict():
            if devices.get_stat(addr, 'available') == devices.AVAILABLE_OFFLINE:
                devices.set_stat(addr, 'available', devices.AVAILABLE_ONLINE)
                devices.set_stat(addr, 'time', int(time.time()))
                message = 'Trying to reach device %s which is currently offline' % devices.get_name(addr)
            commands.add(addr, CommandStatus())
        print('HTTP: %d update_stats' % addr)
        if message is not None:
            response.content_type = 'application/json'
            return json.dumps({
                'message': message
            })

    def request_settings(self):
        addr = int(request.json.get('addr'))
        layout = devices.get_setting(addr, 'ff')
        if layout is not None:
            devices.reset_device_settings(addr)
            for field in get_eeprom_layout(int('0x' + layout, 16)):
                commands.add(addr, CommandGetSetting(field['idx']))
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
                if new != value and CommandSetSetting.valid(settings['ff'], idx, value):
                    commands.add(addr, CommandSetSetting(idx, new))
        print('HTTP: %d set_settings' % addr)

    def reboot(self, addr):
        if devices.get_name(addr) is not None:
            commands.add(addr, CommandReboot())
        print('HTTP: %d reboot' % addr)


    def get_stats(self):
        response.content_type = 'application/json'
        return json.dumps(devices.get_devices_dict())

    def shutdown(self):
        self.server.stop()


httpd = Httpd()
route('/static/<filepath:path>')(httpd.server_static)
route('/')(httpd.index)
route('/temp', method='POST')(httpd.set_temp)
route('/mode', method='POST')(httpd.set_mode)
route('/stats', method='GET')(httpd.get_stats)
route('/update', method='POST')(httpd.update_stats)
route('/request_settings', method='POST')(httpd.request_settings)
route('/settings/<addr:int>', method='GET')(httpd.settings)
route('/settings/<addr:int>', method='POST')(httpd.set_settings)
route('/reboot/<addr:int>', method='POST')(httpd.reboot)
