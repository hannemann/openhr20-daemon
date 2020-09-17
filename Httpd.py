from bottle import ServerAdapter, route, template, static_file, request, response
import bottle
import sys
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

    @staticmethod
    def server_static(filepath):
        return static_file(filepath, root=httpd_path + 'assets/dist')

    @staticmethod
    def index():
        return template('index', title='OpenHR20', devices=devices.get_devices())

    @staticmethod
    def set_temp(addr):
        temp = float(request.json.get('temp'))
        try:
            devices.get_device(addr).set_temperature(temp)
        except KeyError:
            pass
        except ValueError:
            pass
        print('HTTP: %d temp %f' % (addr, temp))

    @staticmethod
    def set_mode(addr):
        mode = request.json.get('mode')
        try:
            devices.get_device(addr).set_mode(mode)
        except KeyError:
            pass
        except ValueError:
            pass
        print('HTTP: %d mode %s' % (addr, mode))

    @staticmethod
    def update_stats(addr):
        try:
            devices.get_device(addr).update_stats()
        except KeyError:
            pass
        except ValueError:
            pass
        print('HTTP: %d update_stats' % addr)

    @staticmethod
    def reboot(addr):
        try:
            devices.get_device(addr).reboot_device()
        except KeyError:
            pass
        except ValueError:
            pass
        print('HTTP: %d reboot' % addr)

    @staticmethod
    def request_settings(addr):
        try:
            devices.get_device(addr).request_settings()
        except KeyError:
            pass
        print('HTTP: %d request_settings' % addr)

    @staticmethod
    def settings(addr):
        try:
            settings = devices.get_device(addr).settings
            if 'ff' in settings:
                layout = get_eeprom_layout(int('0x' + settings['ff'], 16))
                return template('settings', title='Settings', layout=layout, device_settings=settings)
        except KeyError:
            pass
        print('HTTP: %d settings' % addr)

    @staticmethod
    def set_settings(addr):
        try:
            device = devices.get_device(addr)
            for idx, value in device.settings.items():
                new = request.json.get(idx)
                if new != value:
                    device.send_setting(idx, new)
        except KeyError:
            pass
        print('HTTP: %d set_settings' % addr)

    @staticmethod
    def request_timers(addr):
        devices.get_device(addr).request_timers()
        print('HTTP: %d request_timers' % addr)

    @staticmethod
    def timers(addr):
        try:
            device = devices.get_device(addr)
            mode = device.settings['01']
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
        print('HTTP: %d timers' % addr)

    @staticmethod
    def set_timers(addr):
        try:
            device = devices.get_device(addr)
            timers = device.timers
            for day, value in request.json.items():
                if timers[int(day[0])][int(day[1])] != value:
                    device.send_timer(day, value)
        except KeyError:
            pass
        print('HTTP: %d set_timers' % addr)

    @staticmethod
    def get_stats():
        response.content_type = 'application/json'
        return json.dumps(devices.get_devices())

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
