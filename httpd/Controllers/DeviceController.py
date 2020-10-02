from bottle import route, response, request
import json
from Devices import devices


class DeviceController:

    def __init__(self):
        route('/stats', method='GET')(self.get_stats)
        route('/add_device/<addr:int>', method='POST')(self.add_device)
        route('/remove_device/<addr:int>', method='POST')(self.remove_device)
        route('/add_group', method='POST')(self.add_group)
        route('/remove_group', method='POST')(self.remove_group)
        route('/add_device_to_group/<addr:int>', method='POST')(self.add_device_to_group)
        route('/remove_device_from_group/<addr:int>', method='POST')(self.remove_device_from_group)

    @staticmethod
    def get_stats():
        response.content_type = 'application/json'
        devs = {}
        for addr, device in devices.get_devices(with_remote=True).items():
            devs[addr] = device.get_data()
        return json.dumps(devs)

    @staticmethod
    def add_device(addr):
        try:
            group = devices.groups[request.json.get('group')] if 'group' in request.json else None
        except KeyError:
            group = None
        try:
            name = request.json.get('name')
            devices.add_device(
                addr, name,
                json.loads(devices.get_initial_stats(addr)),
                json.loads(devices.get_initial_timers()),
                {}, group
            )
        except KeyError:
            pass

    @staticmethod
    def remove_device(addr):
        try:
            devices.remove_device(addr)
        except KeyError:
            pass

    @staticmethod
    def add_group():
        try:
            name = request.json.get('name')
            devices.add_group(name.lower(), name, [])
        except KeyError:
            pass

    @staticmethod
    def remove_group():
        try:
            key = request.json.get('key')
            devices.remove_group(key)
        except KeyError:
            pass

    @staticmethod
    def add_device_to_group(addr):
        try:
            key = request.json.get('key')
            devices.add_device_to_group(addr, key)
        except KeyError:
            pass

    @staticmethod
    def remove_device_from_group(addr):
        try:
            key = request.json.get('key')
            devices.remove_device_from_group(addr, key)
        except KeyError:
            pass
