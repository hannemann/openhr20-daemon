import paho.mqtt.client as mqtt
from Commands import commands
import time
import threading


class MQTT (threading.Thread):

    count = 0

    def __init__(self):
        threading.Thread.__init__(self)
        commands.push('lala')
        print('MQTT initialized')

    def run(self):
        while True:
            time.sleep(5)
            self.count += 1
            commands.test(' # MQTT {}'.format(self.count))
