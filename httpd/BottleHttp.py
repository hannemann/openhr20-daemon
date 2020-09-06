from bottle import route, run, template, static_file
import bottle
import sys
from Config import config
from Devices import get_devices_dict

debug = config.getboolean('openhr20', 'debug')
bottle.TEMPLATE_PATH.insert(0, './httpd/views/')
bottle.debug(debug)


def run_http():
    run(host='0.0.0.0', port=8020, reloader=debug)
    print('HTTP Server stopped...')
    sys.stdout.flush()


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./httpd/assets/dist')


@route('/')
def index():
    return template('index', title='OpenHR20', devices=get_devices_dict())
