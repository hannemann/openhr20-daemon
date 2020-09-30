from bottle import route, response
import json
from Devices import devices


class DeviceController:

    def __init__(self):
        route('/stats', method='GET')(self.get_stats)

    @staticmethod
    def get_stats():
        response.content_type = 'application/json'
        devs = {}
        for addr, device in devices.get_devices().items():
            devs[addr] = device.get_data()
        return json.dumps(devs)
