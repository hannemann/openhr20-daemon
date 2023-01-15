import sys
from bottle import route, request
from MQTT import mqtt
from WebSocket import ws
from Devices import devices
from httpd.Controllers.RemoteController import RemoteController


class CommandsController:

    def __init__(self):
        route('/temp/<addr:int>', method='POST')(self.set_temp)
        route('/mode/<addr:int>', method='POST')(self.set_mode)
        route('/update/<addr:int>', method='POST')(self.update_stats)
        route('/request_settings/<addr:int>', method='POST')(self.request_settings)
        route('/settings/<addr:int>', method='POST')(self.set_settings)
        route('/request_timers/<addr:int>', method='POST')(self.request_timers)
        route('/set_timers/<addr:int>', method='POST')(self.set_timers)
        route('/reboot/<addr:int>', method='POST')(self.reboot)
        route('/cancel/<addr:int>', method='POST')(self.cancel_commands)

    @staticmethod
    def set_temp(addr):
        temp = float(request.json.get('temp'))
        try:
            if devices.is_remote_device(addr):
                RemoteController.redirect_command(request, addr)
            else:
                device = devices.get_device(addr)
                device.set_temperature(temp)
                if device.group is not None:
                    for dev in device.group.devices:
                        mqtt.publish_availability(dev)
                        ws.send_device_stats(dev)
                else:
                    mqtt.publish_availability(device)
                    ws.send_device_stats(device)

        except KeyError:
            pass
        except ValueError:
            pass
        print(' < HTTP: {} temp {}'.format(addr, temp))
        sys.stdout.flush()

    @staticmethod
    def set_mode(addr):
        mode = request.json.get('mode')
        try:
            if devices.is_remote_device(addr):
                RemoteController.redirect_command(request, addr)
            else:
                device = devices.get_device(addr)
                device.set_mode(mode)
                if device.group is not None:
                    for dev in device.group.devices:
                        mqtt.publish_availability(dev)
                        ws.send_device_stats(dev)
                else:
                    mqtt.publish_availability(device)
                    ws.send_device_stats(device)
        except KeyError:
            pass
        except ValueError:
            pass
        print(' < HTTP: {} mode {}'.format(addr, mode))
        sys.stdout.flush()

    @staticmethod
    def update_stats(addr):
        try:
            if devices.is_remote_device(addr):
                RemoteController.redirect_command(request, addr)
            else:
                device = devices.get_device(addr)
                device.update_stats()
                mqtt.publish_availability(device)
                ws.send_device_stats(device)
        except KeyError:
            pass
        except ValueError:
            pass
        print(' < HTTP: {} update_stats'.format(addr))
        sys.stdout.flush()

    @staticmethod
    def reboot(addr):
        try:
            if devices.is_remote_device(addr):
                RemoteController.redirect_command(request, addr)
            else:
                device = devices.get_device(addr)
                device.reboot_device()
                mqtt.publish_availability(device)
                ws.send_device_stats(device)
        except KeyError:
            pass
        except ValueError:
            pass
        print(' < HTTP: {} reboot'.format(addr))
        sys.stdout.flush()

    @staticmethod
    def request_settings(addr):
        try:
            if devices.is_remote_device(addr):
                RemoteController.redirect_command(request, addr)
            else:
                device = devices.get_device(addr)
                device.request_settings()
                mqtt.publish_availability(device)
                ws.send_device_stats(device)
        except KeyError:
            pass
        print(' < HTTP: {} request_settings'.format(addr))
        sys.stdout.flush()

    @staticmethod
    def set_settings(addr):
        try:
            if devices.is_remote_device(addr):
                RemoteController.redirect_command(request, addr)
            else:
                device = devices.get_device(addr)
                for idx, value in device.settings.items():
                    new = request.json.get(idx)
                    if new != value:
                        device.send_setting(idx, new)
                mqtt.publish_availability(device)
                ws.send_device_stats(device)
        except KeyError:
            pass
        print(' < HTTP: {} set_settings'.format(addr))
        sys.stdout.flush()

    @staticmethod
    def request_timers(addr):
        try:
            if devices.is_remote_device(addr):
                RemoteController.redirect_command(request, addr)
            else:
                device = devices.get_device(addr)
                device.request_timers()
                mqtt.publish_availability(device)
                ws.send_device_stats(device)
        except KeyError:
            pass
        print(' < HTTP: {} request_timers'.format(addr))
        sys.stdout.flush()

    @staticmethod
    def set_timers(addr):
        try:
            if devices.is_remote_device(addr):
                RemoteController.redirect_command(request, addr)
            else:
                device = devices.get_device(addr)
                timers = device.timers
                for day, value in request.json['timers'].items():
                    if timers[int(day[0])][int(day[1])] != value:
                        device.send_timer(day, value)
                new_mode = int(request.json['mode'])
                if new_mode != (0 if int(device.settings['22'], 16) == 0 else 1):
                    device.send_setting('22', '{:02x}'.format(new_mode))
                mqtt.publish_availability(device)
                ws.send_device_stats(device)
        except KeyError:
            pass
        print(' < HTTP: {} set_timers'.format(addr))
        sys.stdout.flush()

    @staticmethod
    def cancel_commands(addr):
        try:
            if devices.is_remote_device(addr):
                RemoteController.redirect_command(request, addr)
            else:
                device = devices.get_device(addr)
                device.cancel_commands()
                mqtt.publish_availability(device)
                ws.send_device_stats(device)
        except KeyError:
            pass
        print(' < HTTP: {} cancel_commands'.format(addr))
        sys.stdout.flush()
