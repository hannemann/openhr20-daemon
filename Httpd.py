from bottle import ServerAdapter, route, template, static_file, request
import bottle
import sys
from Commands.Commands import commands
from Commands.CommandTemperature import CommandTemperature
from Commands.CommandMode import CommandMode
import pathlib
from Config import config
from Devices import get_devices_dict
import threading

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
        self.server = MyWSGIRefServer(port=8020)
        bottle.run(host='0.0.0.0', server=self.server, reloader=False)
        print('HTTP Server stopped...')
        sys.stdout.flush()

    def server_static(self, filepath):
        return static_file(filepath, root=httpd_path + 'assets/dist')

    def index(self):
        return template('index', title='OpenHR20', devices=get_devices_dict())

    def set_temp(self):
        addr = int(request.json.get('addr'))
        temp = float(request.json.get('temp'))
        if addr in get_devices_dict() and CommandTemperature.valid(temp):
            commands.add(addr, CommandTemperature(temp))
        print('HTTP: %d temp %f' % (addr, temp))

    def set_mode(self):
        addr = int(request.json.get('addr'))
        mode = request.json.get('mode')
        if addr in get_devices_dict() and CommandMode.valid(mode):
            commands.add(addr, CommandMode(mode))
        print('HTTP: %d mode %s' % (addr, mode))

    def shutdown(self):
        self.server.stop()


httpd = Httpd()
route('/static/<filepath:path>')(httpd.server_static)
route('/')(httpd.index)
route('/temp', method='POST')(httpd.set_temp)
route('/mode', method='POST')(httpd.set_mode)
