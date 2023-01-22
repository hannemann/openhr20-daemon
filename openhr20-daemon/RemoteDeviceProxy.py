import __init__ as daemon
import os
import sys
import json
import websocket
import time
import threading


class RemoteDeviceProxy(threading.Thread):

    debug = os.getenv('WS_DEBUG') == 'true'
    pendingTasks = set()
    shutting_down = False

    def __init__(self, uri):
        super().__init__()
        self.URI = 'ws://{}'.format(uri)

    def run(self):
        print('WS Proxy: Run {}'.format(self.URI))
        self.client = websocket.WebSocketApp(self.URI, on_open=self.on_open, on_message=self.on_message, on_close=self.on_close, on_error=self.on_error)
        self.client.run_forever()

    def on_open(self, ws):
        print("WS Proxy: Connected to remote daemon at {}".format(self.URI))
        self.send('{"type": "update_stats"}')

    def on_close(self, ws, close_status_code, close_msg):
        if self.shutting_down == False:
            print("Connection to remote daemon {} closed. Attempting reconnect in 10s...".format(self.URI))
            time.sleep(10)
            self.run()
        

    def on_error(self, ws, error):
        print('WS Proxy: {}'.format(error))

    def on_message(self, ws, message):
        if self.debug:
            print(' > WS Proxy {}: {}'.format(self.URI, message))
            sys.stdout.flush()
        daemon.ws.queue.append(json.loads(message))

    def send(self, message):
        if self.debug:
            print(' > WS Proxy {}: {}'.format(self.URI, message))
            sys.stdout.flush()
        try:
            if self.debug:
                print('> WS Proxy OUT (was: {}): {}'.format(type(message), message if type(message) is str else json.dumps(message)))
            self.client.send(message if type(message) is str else json.dumps(message))
        except TypeError as e:
            print(e)
            pass

    def shutdown(self):
        if self.debug:
            print('\nWS Proxy: Closing connection to remote daemon {}'.format(self.URI))
            sys.stdout.flush()
        self.shutting_down = True
        self.client.close()
