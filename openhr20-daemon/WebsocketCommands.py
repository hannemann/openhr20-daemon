import __init__ as daemon
import os, sys

class WebsocketCommands:

    @staticmethod
    def set_temp(addr, temp):
        try:
            if daemon.devices.is_remote_device(addr):
              print('TODO: send command to remote device')
            else:
                device = daemon.devices.get_device(addr)
                device.set_temperature(temp)
                if device.group is not None:
                    for dev in device.group.devices:
                        daemon.mqtt.publish_availability(dev)
                        daemon.ws.send_device_stats(dev)
                else:
                    daemon.mqtt.publish_availability(device)
                    daemon.ws.send_device_stats(device)

        except KeyError:
            pass
        except ValueError:
            pass
        if os.getenv('WS_DEBUG') == 'true':
            print(' < WS: {} temp {}'.format(addr, temp))
            sys.stdout.flush()

    @staticmethod
    def set_mode(addr, mode):
        try:
            if daemon.devices.is_remote_device(addr):
              print('TODO: send command to remote device')
            else:
                device = daemon.devices.get_device(addr)
                device.set_mode(mode)
                if device.group is not None:
                    for dev in device.group.devices:
                        daemon.mqtt.publish_availability(dev)
                        daemon.ws.send_device_stats(dev)
                else:
                    daemon.mqtt.publish_availability(device)
                    daemon.ws.send_device_stats(device)
        except KeyError:
            pass
        except ValueError:
            pass
        if os.getenv('WS_DEBUG') == 'true':
            print(' < WS: {} mode {}'.format(addr, mode))
            sys.stdout.flush()

    @staticmethod
    def update_stats(addr):
        try:
            if daemon.devices.is_remote_device(addr):
              print('TODO: send command to remote device')
            else:
                device = daemon.devices.get_device(addr)
                device.update_stats()
                daemon.mqtt.publish_availability(device)
                daemon.ws.send_device_stats(device)
        except KeyError:
            pass
        except ValueError:
            pass
        if os.getenv('WS_DEBUG') == 'true':
            print(' < WS: {} update_stats'.format(addr))
            sys.stdout.flush()

    @staticmethod
    def cancel_commands(addr):
        try:
            if daemon.devices.is_remote_device(addr):
              print('TODO: send command to remote device')
            else:
                device = daemon.devices.get_device(addr)
                device.cancel_commands()
                daemon.mqtt.publish_availability(device)
                daemon.ws.send_device_stats(device)
        except KeyError:
            pass