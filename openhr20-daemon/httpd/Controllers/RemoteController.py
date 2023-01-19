from bottle import route, response
from Devices import devices
import pickle
import http.client


class RemoteController:

    def __init__(self):
        route('/device/serialized/<addr:int>', method='GET')(self.get_device_serialized)
        route('/group/serialized/<name>', method='GET')(self.get_group_serialized)

    @staticmethod
    def get_device_serialized(addr):
        response.content_type = 'application/octet-stream'
        try:
            device = devices.get_device(addr)
            return pickle.dumps(device)
        except KeyError:
            pass

    @staticmethod
    def get_group_serialized(name):
        response.content_type = 'application/octet-stream'
        try:
            group = devices.groups[name]
            return pickle.dumps(group)
        except KeyError:
            pass

    @staticmethod
    def redirect_command(req, addr):
        remote = devices.get_remote(addr)
        conn = http.client.HTTPConnection(remote)
        conn.request(req.method, req.fullpath, req.body.read().decode('utf-8'), dict(req.headers))
        conn.close()
