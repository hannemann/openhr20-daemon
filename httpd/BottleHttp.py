from bottle import route, run, template, static_file
import bottle
import sys
from Config import config

bottle.TEMPLATE_PATH.insert(0, './httpd/views/')
bottle.debug(True)


@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./httpd/assets/dist')

@route('/')
def index():
    return template('index', title='Lala?')


def run_http():
    run(host='0.0.0.0', port=8020, reloader=True)
    print('HTTP Server stopped...')
    sys.stdout.flush()
