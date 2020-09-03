import paho.mqtt.client as mqtt
from Commands import commands
import time
import threading


class MQTT (threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        commands.push('lala')
        print('MQTT initialized')

    def run(self):
        while True:
            time.sleep(5)
            print(' # MQTT')
