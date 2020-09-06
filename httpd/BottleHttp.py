from bottle import route, run, template
import sys
from Config import config


@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}', name=name)


def run_http():
    run(host='0.0.0.0', port=8020)
    print('HTTP Server stopped...')
    sys.stdout.flush()
