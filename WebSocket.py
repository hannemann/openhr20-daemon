import asyncio
import websockets
from Config import config, defaults
import threading
import json


class WebSocket(threading.Thread):

    connected = set()

    def __init__(self):
        super().__init__()
        self.listen_address = config.get('ws', 'listen_address', fallback=defaults['ws']['listen_address'])
        self.port = config.getint('ws', 'port', fallback=defaults['ws']['port'])
        self.loop = asyncio.get_event_loop()
        self.server = websockets.serve(self.listen, self.listen_address, self.port)
        self.loop.run_until_complete(self.server)

    def run(self):
        print('Websocket: Start listening on %s:%s...' % (self.listen_address, str(self.port)))
        self.loop.run_forever()
        print('Websocket: Loop stopped')

    async def listen(self, websocket, path):
        self.connected.add(websocket)
        try:
            while True:
                message = await websocket.recv()
                print(message)
        # except ConnectionClosedError:
        #    pass
        finally:
            self.connected.remove(websocket)

    def send(self, message):
        for websocket in self.connected:
            self.loop.create_task(websocket.send(message))

    def send_device_stats(self, device):
        stats = device.get_stats()
        self.send(json.dumps(stats))

    def shutdown(self):
        self.loop.call_soon_threadsafe(self.loop.stop)


ws = WebSocket()
