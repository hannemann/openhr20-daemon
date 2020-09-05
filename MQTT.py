import sys

import paho.mqtt.client as mqttc
from Commands import commands
import threading
from CommandTemperature import CommandTemperature
from CommandMode import CommandMode
from Config import config


class MQTT (threading.Thread):

    daemon = True
    count = 0
    mode = 'mode'
    temp = 'temp'

    def __init__(self):
        threading.Thread.__init__(self)
        self.client = mqttc.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(config['mqtt'].get('host'), int(config['mqtt'].get('port')), 60)
        print('MQTT initialized')
        sys.stdout.flush()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT Broker with result code " + str(rc))
        sys.stdout.flush()
        #self.client.subscribe("$SYS/#")
        cmnd_topic = config['mqtt'].get('cmnd_topic').strip('/') + "/#"
        self.client.subscribe(cmnd_topic)
        print('MQTT: Subscribed to topic %s' % cmnd_topic)
        sys.stdout.flush()

    def on_message(self, client, userdata, msg):
        topic = msg.topic.replace(config['mqtt'].get('cmnd_topic').strip('/') + '/', '').split('/')
        cmnd = topic[0]
        addr = int(topic[1], 10)
        print("MQTT: %d %s %s" % (addr, cmnd, msg.payload.decode('utf_8').strip()))
        sys.stdout.flush()

        if 0 < addr < 30:
            payload = msg.payload.decode('utf_8').strip()
            if cmnd == self.mode:
                commands.add(addr, CommandMode(payload))
            elif cmnd == self.temp:
                commands.add(addr, CommandTemperature(payload))

    def publish(self,
                topic,
                payload,
                qos=int(config['mqtt'].get('qos', 0)),
                retain=config['mqtt'].getboolean('retain', False)
                ):
        self.client.publish(topic, payload, qos, retain)

    def run(self):
        self.client.loop_forever()

    def shutdown(self):
        self.client.loop_stop()
        self.client.disconnect()
        print('MQTT connection closed')
        sys.stdout.flush()


mqtt = MQTT()
