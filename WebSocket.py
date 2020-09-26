import asyncio
import websockets
from Config import config, defaults
import threading
import json
from collections import deque


class WebSocket(threading.Thread):

    connected = set()
    queue = deque([])

    def __init__(self):
        super().__init__()
        self.listen_address = config.get('ws', 'listen_address', fallback=defaults['ws']['listen_address'])
        self.port = config.getint('ws', 'port', fallback=defaults['ws']['port'])
        self.loop = asyncio.get_event_loop()
        self.server = websockets.serve(self.connect, self.listen_address, self.port)
        self.loop.run_until_complete(self.server)

    def run(self):
        print('Websocket: Start listening on %s:%s...' % (self.listen_address, str(self.port)))
        self.loop.create_task(self.send())
        self.loop.run_forever()
        print('Websocket: Loop stopped')

    async def connect(self, websocket, path):
        self.connected.add(websocket)
        try:
            while self.loop.is_running():
                message = await websocket.recv()
                print(message)
        except websockets.exceptions.ConnectionClosedOK:
            pass
        finally:
            self.connected.remove(websocket)

    async def send(self):
        while self.loop.is_running():
            if len(self.queue) > 0:
                message = self.queue.popleft()
                for websocket in self.connected:
                    await websocket.send(message)
            await asyncio.sleep(0.1)

    def send_device_stats(self, device):
        stats = device.get_stats()
        self.queue.append(json.dumps(stats))

    def shutdown(self):
        self.loop.call_soon_threadsafe(self.loop.stop)


ws = WebSocket()
