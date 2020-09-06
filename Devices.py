import configparser
import os

file = './devices.conf'
devices = configparser.ConfigParser()


def write_file():
    fd = open(file, 'w')
    devices.write(fd)
    fd.close()


if not os.path.exists(file):
    devices['names'] = {
        '10': 'Livingroom',
        '11': 'Bathroom'
    }
    devices['stats'] = {}
    devices['timer'] = {}
    devices['settings'] = {}

    write_file()
else:
    devices.read(file)
