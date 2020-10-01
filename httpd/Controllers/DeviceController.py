from bottle import route, response, request
import json
from Devices import devices


class DeviceController:

    def __init__(self):
        route('/stats', method='GET')(self.get_stats)
        route('/add_device/<addr:int>', method='POST')(self.add_device)
        route('/remove_device/<addr:int>', method='POST')(self.remove_device)

    @staticmethod
    def get_stats():
        response.content_type = 'application/json'
        devs = {}
        for addr, device in devices.get_devices().items():
            devs[addr] = device.get_data()
        return json.dumps(devs)

    @staticmethod
    def add_device(addr):
        name = request.json.get('name')
        group = devices.groups[request.json.get('group')] if 'group' in request.json else None
        devices.add_device(
            addr, name,
            json.loads(devices.get_initial_stats(addr)),
            json.loads(devices.get_initial_timers()),
            {}, group
        )

    @staticmethod
    def remove_device(addr):
        try:
            devices.remove_device(addr)
        except KeyError:
            pass
