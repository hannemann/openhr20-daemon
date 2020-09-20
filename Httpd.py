import pickle
from bottle import ServerAdapter, route, template, static_file, request, response
import bottle
import sys
import pathlib
from Config import config, defaults
from Devices import devices
import threading
import json
from Eeprom import get_eeprom_layout
from MQTT import mqtt
import http.client

debug = config.getboolean('openhr20', 'debug', fallback='no')
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
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        # self.server.server_close() <--- alternative but causes bad fd exception
        self.server.shutdown()


class Httpd(threading.Thread):

    server = None

    def run(self):
        host = config.get('httpd', 'host', fallback=defaults['httpd']['host'])
        port = config.getint('httpd', 'port', fallback=defaults['httpd']['port'])
        self.server = MyWSGIRefServer(port=port, host=host)
        bottle.run(server=self.server, reloader=False)
        print('HTTP Server stopped...')
        sys.stdout.flush()

    @staticmethod
    def server_static(filepath):
        return static_file(filepath, root=httpd_path + 'assets/dist')

    @staticmethod
    def index():
        groups = sorted(devices.get_groups().values(), key=lambda g: g.name)
        ungrouped = sorted([d for d in devices.get_devices().values() if d.group is None], key=lambda d: d.name)

        return template('index', title='OpenHR20', ungrouped_devices=ungrouped, groups=groups)

    @staticmethod
    def groups():
        ungrouped = [d for d in devices.devices.values() if d.group is None]
        return template('groups', title='Groups', ungrouped_devices=ungrouped, groups=devices.groups.values())

    @staticmethod
    def set_temp(addr):
        temp = float(request.json.get('temp'))
        try:
            if devices.has_proxy(addr):
                Httpd.redirect_to_proxy(request, addr)
            else:
                device = devices.get_device(addr)
                device.set_temperature(temp)
                for dev in device.group.devices:
                    mqtt.publish_availability(dev)
        except KeyError:
            pass
        except ValueError:
            pass
        print('HTTP: %d temp %f' % (addr, temp))

    @staticmethod
    def set_mode(addr):
        mode = request.json.get('mode')
        try:
            if devices.has_proxy(addr):
                Httpd.redirect_to_proxy(request, addr)
            else:
                device = devices.get_device(addr)
                device.set_mode(mode)
                for dev in device.group.devices:
                    mqtt.publish_availability(dev)
        except KeyError:
            pass
        except ValueError:
            pass
        print('HTTP: %d mode %s' % (addr, mode))

    @staticmethod
    def update_stats(addr):
        try:
            if devices.has_proxy(addr):
                Httpd.redirect_to_proxy(request, addr)
            else:
                device = devices.get_device(addr)
                device.update_stats()
                mqtt.publish_availability(device)
        except KeyError:
            pass
        except ValueError:
            pass
        print('HTTP: %d update_stats' % addr)

    @staticmethod
    def reboot(addr):
        try:
            if devices.has_proxy(addr):
                Httpd.redirect_to_proxy(request, addr)
            else:
                device = devices.get_device(addr)
                device.reboot_device()
                mqtt.publish_availability(device)
        except KeyError:
            pass
        except ValueError:
            pass
        print('HTTP: %d reboot' % addr)

    @staticmethod
    def request_settings(addr):
        try:
            if devices.has_proxy(addr):
                Httpd.redirect_to_proxy(request, addr)
            else:
                device = devices.get_device(addr)
                device.request_settings()
                mqtt.publish_availability(device)
        except KeyError:
            pass
        print('HTTP: %d request_settings' % addr)

    @staticmethod
    def settings(addr):
        try:
            if devices.has_proxy(addr):
                settings = devices.get_device_from_proxy(addr).settings
            else:
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
            if devices.has_proxy(addr):
                Httpd.redirect_to_proxy(request, addr)
            else:
                device = devices.get_device(addr)
                for idx, value in device.settings.items():
                    new = request.json.get(idx)
                    if new != value:
                        device.send_setting(idx, new)
                mqtt.publish_availability(device)
        except KeyError:
            pass
        print('HTTP: %d set_settings' % addr)

    @staticmethod
    def request_timers(addr):
        try:
            if devices.has_proxy(addr):
                Httpd.redirect_to_proxy(request, addr)
            else:
                device = devices.get_device(addr)
                device.request_timers()
                mqtt.publish_availability(device)
        except KeyError:
            pass
        print('HTTP: %d request_timers' % addr)

    @staticmethod
    def timers(addr):
        try:
            if devices.has_proxy(addr):
                device = devices.get_device_from_proxy(addr)
            else:
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
            if devices.has_proxy(addr):
                Httpd.redirect_to_proxy(request, addr)
            else:
                device = devices.get_device(addr)
                timers = device.timers
                for day, value in request.json.items():
                    if timers[int(day[0])][int(day[1])] != value:
                        device.send_timer(day, value)
                mqtt.publish_availability(device)
        except KeyError:
            pass
        print('HTTP: %d set_timers' % addr)

    @staticmethod
    def get_stats():
        response.content_type = 'application/json'
        devs = {}
        for addr, device in devices.get_devices().items():
            devs[addr] = device.get_data()
        return json.dumps(devs)

    @staticmethod
    def get_device_serialized(addr):
        response.content_type = 'application/octet-stream'
        try:
            device = devices.get_device(addr)
            return pickle.dumps(device)
        except KeyError:
            pass

    @staticmethod
    def get_group_serialized(name):
        response.content_type = 'application/octet-stream'
        try:
            group = devices.groups[name]
            return pickle.dumps(group)
        except KeyError:
            pass

    @staticmethod
    def redirect_to_proxy(req, addr):
        proxy = devices.get_proxy(addr)
        conn = http.client.HTTPConnection(proxy)
        conn.request(req.method, req.fullpath, req.body.read().decode('utf-8'), dict(req.headers))
        conn.close()

    def shutdown(self):
        self.server.stop()


httpd = Httpd()
route('/static/<filepath:path>')(httpd.server_static)
route('/')(httpd.index)
route('/groups')(httpd.groups)
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
route('/device/serialized/<addr:int>', method='GET')(httpd.get_device_serialized)
route('/group/serialized/<name>', method='GET')(httpd.get_group_serialized)
