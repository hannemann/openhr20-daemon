from bottle import ServerAdapter
import bottle
import sys
import os
import pathlib
import threading

httpd_path = '/' + str(pathlib.Path(__file__).parent.absolute()).strip('/') + '/httpd/'
bottle.TEMPLATE_PATH.insert(0, httpd_path + 'views')
bottle.debug(os.getenv('HTTP_DEBUG') == 'true')


class MyWSGIRefServer(ServerAdapter):
    """
    for shutting down cleanly
    https://stackoverflow.com/a/16056443
    """
    server = None

    def run(self, handler):
        if os.getenv('HTTP_DEBUG') == 'true':
            print('HTTP Debug enabled')
            sys.stdout.flush()
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
        host = os.getenv("HTTP_LISTEN_ADDRESS")
        port = int(os.getenv("HTTP_PORT"))
        self.server = MyWSGIRefServer(port=port, host=host)
        bottle.run(server=self.server, reloader=False, quiet=os.getenv('HTTP_DEBUG') == 'false')
        print('HTTP Server stopped...')
        sys.stdout.flush()

    def shutdown(self):
        self.server.stop()


