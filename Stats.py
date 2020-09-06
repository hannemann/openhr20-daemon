from MQTT import mqtt
import time
from Commands.Commands import commands
import json
from Config import config


class Stats:

    @staticmethod
    def create_message(addr, response):
        stats = {
            'addr': addr,
        }

        t = 0
        items = response.split(' ')
        for item in items:
            if item[0] == 'A':
                stats['mode'] = 'AUTO'
            elif item[0] == '-':
                stats['mode'] = '-'
            elif item[0] == 'M':
                stats['mode'] = 'MANU'
            elif item[0] == 'S':
                stats['wanted'] = int(item[1:]) / 100
            elif item[0] == 'V':
                stats['valve'] = int(item[1:])
            elif item[0] == 'I':
                stats['real'] = int(item[1:]) / 100
            elif item[0] == 'B':
                stats['battery'] = int(item[1:]) / 1000
            elif item[0] == 'E':
                stats['error'] = int(item[1:], 16)
            elif item[0] == 'W':
                stats['window'] = 'open'
            elif item[0] == 'X':
                stats['force'] = True
            elif item[0] == 'm':
                t += 60 * int(item[1:])
            elif item[0] == 's':
                t += int(item[1:])

        timestamp = int(time.time())
        if timestamp % 3600 < t:
            timestamp -= 3600

        timestamp = int((timestamp / 3600) * 3600 + t)
        stats['time'] = timestamp
        stats['synced'] = not commands.has_command(addr)

        mqtt.publish(
            config['mqtt'].get('stats_topic').strip('/') + '/%d' % addr,
            json.dumps(stats)
        )

        return stats
