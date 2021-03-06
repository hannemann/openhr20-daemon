import time
from Commands.Commands import commands


class Stats:

    @staticmethod
    def create(device, response):
        stats = {
            'addr': device.addr,
        }

        t = 0
        items = response.split(' ')
        for item in items:
            if item[0] == 'A':
                stats['mode'] = 'auto'
            elif item[0] == '-':
                stats['mode'] = '-'
            elif item[0] == 'M':
                stats['mode'] = 'manu'
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
        timestamp -= timestamp % 3600
        timestamp += t
        stats['time'] = timestamp
        stats['synced'] = not commands.has_command(device)

        return stats
