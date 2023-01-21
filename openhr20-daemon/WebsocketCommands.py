from Devices import devices
from WebSocket import ws
from MQTT import mqtt

class WebSocketCommands:

    @staticmethod
    def cancel_commands(addr):
        try:
            if devices.is_remote_device(addr):
              print('TODO: send command to remote device')
            else:
                device = devices.get_device(addr)
                device.cancel_commands()
                mqtt.publish_availability(device)
                ws.send_device_stats(device)
        except KeyError:
            pass