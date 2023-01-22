import asyncio
import websockets
import os
import threading
import json
import sys
from collections import deque
import __init__ as daemon


class WebSocket(threading.Thread):

    connected = set()
    queue = deque([])
    debug = os.getenv('WS_DEBUG') == 'true'

    def __init__(self):
        if self.debug:
            print('Websockets Debug enabled')
            sys.stdout.flush()
        super().__init__()
        self.listen_address = os.getenv("WS_LISTEN_ADDRESS")
        self.port = int(os.getenv("WS_PORT"))
        self.loop = asyncio.get_event_loop()
        self.server = websockets.serve(self.connect, self.listen_address, self.port)
        self.loop.run_until_complete(self.server)

    def run(self):
        print('Websocket: Start listening on {}:{}...'.format(self.listen_address, str(self.port)))
        self.loop.create_task(self.send())
        self.loop.run_forever()
        print('Websocket: Loop stopped')

    async def connect(self, websocket, path):
        if self.debug:
            print(' < WS incoming connection from {}'.format(websocket.remote_address[0]))
            sys.stdout.flush()
        self.connected.add(websocket)
        try:
            while self.loop.is_running():
                message = json.loads(await websocket.recv())
                if self.debug:
                    print(' < WS {}: {}'.format(websocket.remote_address[0], message))
                    sys.stdout.flush()

                if 'type' in message:
                    if message['type'] == 'update_stats':
                        self.queue_all_stats()
                    if 'addr' in message:
                        if message['type'] == 'temp' and 'temp' in message:
                            daemon.WebsocketCommands.set_temp(message)

                        if message['type'] == 'mode' and 'mode' in message:
                            daemon.WebsocketCommands.set_mode(message)

                        if message['type'] == 'update':
                            daemon.WebsocketCommands.update_stats(message)

                        if message['type'] == 'reboot':
                            daemon.WebsocketCommands.reboot(message)

                        if message['type'] == 'request_settings':
                            daemon.WebsocketCommands.request_settings(message)

                        if message['type'] == 'save_settings':
                            daemon.WebsocketCommands.save_settings(message)

                        if message['type'] == 'request_timers':
                            daemon.WebsocketCommands.request_timers(message)

                        if message['type'] == 'save_timers':
                            daemon.WebsocketCommands.save_timers(message)

                        if message['type'] == 'cancel_commands':
                            daemon.WebsocketCommands.cancel_commands(message)

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
                    try:
                        if self.debug:
                            print(' > WS {} {}/{}: {}'.format(
                                websocket.remote_address[0], message['type'], message['addr'], message['payload']))
                            sys.stdout.flush()
                        await websocket.send(json.dumps(message))
                        if self.debug:
                            print(' > WS message sent')
                            sys.stdout.flush()

                    except websockets.exceptions.ConnectionClosedError as e:
                        if self.debug:
                            print('Websocket send: {}'.format(e))
                        pass
                    except websockets.exceptions.ConnectionClosedOK as e:
                        if self.debug:
                            print('Websocket send: {}'.format(e))
                        pass

            await asyncio.sleep(0.1)

    def send_device_stats(self, device):
        stats = device.dict()
        message = {
            "type": "stats",
            "addr": device.addr,
            "payload": stats
        }
        self.queue.append(message)

    def queue_all_stats(self):
        for device in daemon.devices.devices.values():
            self.send_device_stats(device)
        for proxy in daemon.devices.remoteProxies.values():
            proxy.send(json.dumps({'type': 'update_stats'}))

    def shutdown(self):
        if self.debug:
            print('WS shutting down')
            sys.stdout.flush()
        self.loop.call_soon_threadsafe(self.loop.stop)
