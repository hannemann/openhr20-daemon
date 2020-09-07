from bottle import route, run, template, static_file
import bottle
import sys
import os
import pathlib
from Config import config
from Devices import get_devices_dict

debug = config.getboolean('openhr20', 'debug')
httpd_path = '/' + str(pathlib.Path(__file__).parent.absolute()).strip('/')
bottle.TEMPLATE_PATH.insert(0, httpd_path + '/views')
bottle.debug(debug)


def run_http():
    run(host='0.0.0.0', port=8020, reloader=debug)
    print('HTTP Server stopped...')
    sys.stdout.flush()


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=httpd_path + '/assets/dist')


@route('/')
def index():
    return template('index', title='OpenHR20', devices=get_devices_dict())
