class Group:

    name = ''
    devices = []

    def __init__(self, name, devices):
        self.name = name
        self.devices = sorted(devices, key=lambda d: d.name)

    def dict(self):
        d = {
            'name': self.name,
            'devices': [device.addr for device in self.devices]
        }
        return d
