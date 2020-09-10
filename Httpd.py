from bottle import ServerAdapter, route, template, static_file, request, response
import bottle
import sys
from Commands.Commands import commands
from Commands.CommandTemperature import CommandTemperature
from Commands.CommandMode import CommandMode
from Commands.CommandStatus import CommandStatus
import pathlib
from Config import config
from Devices import get_devices_dict
import threading
import json

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

    def update_stats(self):
        addr = int(request.json.get('addr'))
        if addr in get_devices_dict():
            commands.add(addr, CommandStatus())

    def get_stats(self):
        response.content_type = 'application/json'
        return json.dumps(get_devices_dict())

    def shutdown(self):
        self.server.stop()


httpd = Httpd()
route('/static/<filepath:path>')(httpd.server_static)
route('/')(httpd.index)
route('/temp', method='POST')(httpd.set_temp)
route('/mode', method='POST')(httpd.set_mode)
route('/stats', method='GET')(httpd.get_stats)
route('/update', method='POST')(httpd.update_stats)
