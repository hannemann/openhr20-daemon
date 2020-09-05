import paho.mqtt.client as mqttc
from Commands import commands
import threading
from CommandTemperature import CommandTemperature
from CommandMode import CommandMode
from Config import config


class MQTT (threading.Thread):

    daemon = True
    count = 0
    cmndBase = 'cmnd/openhr20-python/'
    mode = 'mode'
    temp = 'temp'

    def __init__(self):
        threading.Thread.__init__(self)
        self.client = mqttc.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(config['mqtt'].get('host'), int(config['mqtt'].get('port')), 60)
        print('MQTT initialized')

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT Broker with result code " + str(rc))
        #self.client.subscribe("$SYS/#")
        self.client.subscribe(config['mqtt'].cmnd_topic.strip('/') + "/#")

    def on_message(self, client, userdata, msg):
        print(msg.topic + " " + msg.payload.decode('utf_8').strip())
        topic = msg.topic.replace(self.cmndBase, '').split('/')
        cmnd = topic[0]
        addr = int(topic[1], 10)

        if 0 < addr < 30:
            payload = msg.payload.decode('utf_8').strip()
            if cmnd == self.mode:
                commands.add(addr, CommandMode(payload))
            elif cmnd == self.temp:
                temperature = int(payload)
                commands.add(addr, CommandTemperature(temperature))

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


mqtt = MQTT()
