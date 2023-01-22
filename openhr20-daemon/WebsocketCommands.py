import __init__ as daemon
import os, sys

class WebsocketCommands:

    @staticmethod
    def set_temp(message):
        try:
            if daemon.devices.is_remote_device(str(message['addr'])):
                WebsocketCommands.redirect_command(message)
            else:
                device = daemon.devices.get_device(str(message['addr']))
                device.set_temperature(str(message['temp']))
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
            print(' < WS: {} temp {}'.format(str(message['addr']), str(message['temp'])))
            sys.stdout.flush()

    @staticmethod
    def set_mode(message):
        try:
            if daemon.devices.is_remote_device(str(message['addr'])):
                WebsocketCommands.redirect_command(message)
            else:
                device = daemon.devices.get_device(str(message['addr']))
                device.set_mode(str(message['mode']))
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
            print(' < WS: {} mode {}'.format(str(message['addr']), str(message['mode'])))
            sys.stdout.flush()

    @staticmethod
    def update_stats(message):
        try:
            if daemon.devices.is_remote_device(str(message['addr'])):
                WebsocketCommands.redirect_command(message)
            else:
                device = daemon.devices.get_device(str(message['addr']))
                device.update_stats()
                daemon.mqtt.publish_availability(device)
                daemon.ws.send_device_stats(device)
        except KeyError:
            pass
        except ValueError:
            pass
        if os.getenv('WS_DEBUG') == 'true':
            print(' < WS: {} update_stats'.format(message))
            sys.stdout.flush()

    @staticmethod
    def reboot(message):
        try:
            if daemon.devices.is_remote_device(str(message['addr'])):
                WebsocketCommands.redirect_command(message)
            else:
                device = daemon.devices.get_device(str(message['addr']))
                device.reboot_device()
                daemon.mqtt.publish_availability(device)
                daemon.ws.send_device_stats(device)
        except KeyError:
            pass
        except ValueError:
            pass
        if os.getenv('WS_DEBUG') == 'true':
            print(' < WS: {} reboot'.format(str(message['addr'])))
            sys.stdout.flush()

    @staticmethod
    def request_settings(message):
        try:
            if daemon.devices.is_remote_device(str(message['addr'])):
                WebsocketCommands.redirect_command(message)
            else:
                device = daemon.devices.get_device(str(message['addr']))
                device.request_settings()
                daemon.mqtt.publish_availability(device)
                daemon.ws.send_device_stats(device)
        except KeyError:
            pass
        if os.getenv('WS_DEBUG') == 'true':
            print(' < WS: {} request_settings'.format(str(message['addr'])))
            sys.stdout.flush()

    @staticmethod
    def save_settings(message):
        try:
            if daemon.devices.is_remote_device(str(message['addr'])):
                WebsocketCommands.redirect_command(message)
            else:
                device = daemon.devices.get_device(str(message['addr']))
                for idx, value in device.settings.items():
                    new = message['settings'][idx]
                    if new != value:
                        device.send_setting(idx, new)
                daemon.mqtt.publish_availability(device)
                daemon.ws.send_device_stats(device)
        except KeyError:
            pass
        if os.getenv('WS_DEBUG') == 'true':
            print(' < WS: {} save_settings'.format(str(message['addr'])))
            sys.stdout.flush()

    @staticmethod
    def request_timers(message):
        print('Lalal: {}'.format(message));
        try:
            if daemon.devices.is_remote_device(str(message['addr'])):
                WebsocketCommands.redirect_command(message)
            else:
                device = daemon.devices.get_device(str(message['addr']))
                device.request_timers()
                daemon.mqtt.publish_availability(device)
                daemon.ws.send_device_stats(device)
        except KeyError:
            pass
        if os.getenv('WS_DEBUG') == 'true':
            print(' < WS: {} request_timers'.format(str(message['addr'])))
            sys.stdout.flush()

    @staticmethod
    def save_timers(message):
        try:
            if daemon.devices.is_remote_device(str(message['addr'])):
                WebsocketCommands.redirect_command(message)
            else:
                device = daemon.devices.get_device(str(message['addr']))
                timers = device.timers
                for day, value in message['timers'].items():
                    if timers[int(day[0])][int(day[1])] != value:
                        device.send_timer(day, value)
                new_mode = int(message['mode'])
                if new_mode != (0 if int(device.settings['22'], 16) == 0 else 1):
                    device.send_setting('22', '{:02x}'.format(new_mode))
                daemon.mqtt.publish_availability(device)
                daemon.ws.send_device_stats(device)
        except KeyError:
            pass
        if os.getenv('WS_DEBUG') == 'true':
            print(' < WS: {} save_timers'.format(str(message['addr'])))
            sys.stdout.flush()

    @staticmethod
    def cancel_commands(message):
        try:
            if daemon.devices.is_remote_device(str(message['addr'])):
                WebsocketCommands.redirect_command(message)
            else:
                device = daemon.devices.get_device(str(message['addr']))
                device.cancel_commands()
                daemon.mqtt.publish_availability(device)
                daemon.ws.send_device_stats(device)
        except KeyError:
            pass

    @staticmethod
    def redirect_command(message):
        remote_device = daemon.devices.remoteProxies[str(message['addr'])]
        remote_device.send(message)
        
        