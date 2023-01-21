import __init__ as daemon

class WebsocketCommands:

    @staticmethod
    def cancel_commands(addr, websocket):
        try:
            if daemon.devices.is_remote_device(addr):
              print('TODO: send command to remote device')
            else:
                device = daemon.devices.get_device(addr)
                device.cancel_commands()
                daemon.mqtt.publish_availability(device)
                websocket.send_device_stats(device)
        except KeyError:
            pass