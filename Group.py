class Group:

    key = ''
    name = ''
    devices = []

    def __init__(self, key, name, devices):
        self.key = key
        self.name = name
        self.devices = devices
        self.sort_devices()

    def dict(self):
        d = {
            'key': self.key,
            'name': self.name,
            'devices': [device.addr for device in self.devices]
        }
        return d

    def append(self, device):
        self.devices.append(device)
        self.sort_devices()

    def remove(self, device):
        self.devices.remove(device)

    def sort_devices(self):
        self.devices = sorted(self.devices, key=lambda d: d.name)
