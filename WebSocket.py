import asyncio
import websockets
import os
import threading
import json
from collections import deque
from Devices import devices


class WebSocket(threading.Thread):

    connected = set()
    queue = deque([])

    def __init__(self):
        super().__init__()
        self.listen_address = os.getenv("WS_LISTEN_ADDRESS")
        self.port = int(os.getenv("WS_PORT"))
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
                message = json.loads(await websocket.recv())
                print(message)
                if 'type' in message:
                    if message['type'] == 'update_stats':
                        self.queue_all_stats()

        except websockets.exceptions.ConnectionClosedOK:
            pass
        except websockets.exceptions.ConnectionClosedError:
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
        message = {
            "type": "stats",
            "payload": stats
        }
        self.queue.append(json.dumps(message))

    def queue_all_stats(self):
        for device in devices.devices.values():
            self.send_device_stats(device)

    def shutdown(self):
        self.loop.call_soon_threadsafe(self.loop.stop)


ws = WebSocket()
