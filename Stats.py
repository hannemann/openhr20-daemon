from MQTT import mqtt
import time
from Commands.Commands import commands
import json
from Config import config


class Stats:

    @staticmethod
    def create_message(addr, response):
        message = {
            'addr': addr,
        }

        t = 0
        items = response.split(' ')
        for item in items:
            if item[0] == 'A':
                message['mode'] = 'AUTO'
            elif item[0] == '-':
                message['mode'] = '-'
            elif item[0] == 'M':
                message['mode'] = 'MANU'
            elif item[0] == 'S':
                message['wanted'] = int(item[1:]) / 100
            elif item[0] == 'V':
                message['valve'] = int(item[1:])
            elif item[0] == 'I':
                message['real'] = int(item[1:]) / 100
            elif item[0] == 'B':
                message['battery'] = int(item[1:]) / 1000
            elif item[0] == 'E':
                message['error'] = int(item[1:], 16)
            elif item[0] == 'W':
                message['window'] = 'open'
            elif item[0] == 'X':
                message['force'] = True
            elif item[0] == 'm':
                t += 60 * int(item[1:])
            elif item[0] == 's':
                t += int(item[1:])

        timestamp = int(time.time())
        if timestamp % 3600 < t:
            timestamp -= 3600

        timestamp = int((timestamp / 3600) * 3600 + t)
        message['time'] = timestamp
        message['synced'] = not commands.has_command(addr)

        mqtt.publish(
            config['mqtt'].get('stats_topic').strip('/') + '/%d' % addr,
            json.dumps(message)
        )
