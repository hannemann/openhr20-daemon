import json
import sys
import paho.mqtt.client as mqttc
from Commands.Commands import commands
import threading
from Commands.CommandTemperature import CommandTemperature
from Commands.CommandMode import CommandMode
from Commands.CommandStatus import CommandStatus
from Commands.CommandReboot import CommandReboot
from Config import config
from Devices import devices


class MQTT(threading.Thread):
    daemon = True
    count = 0
    temp = 'temp'

    def __init__(self):
        threading.Thread.__init__(self)
        self.client = mqttc.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        print('MQTT initialized')
        sys.stdout.flush()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to MQTT Broker with result code " + str(rc))
        sys.stdout.flush()
        # self.client.subscribe("$SYS/#")
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

        try:
            payload = msg.payload.decode('utf_8').strip()
            device = devices.get_devices(addr)
            if cmnd == CommandMode.abbr:
                commands.set_mode(device, payload)
            elif cmnd == CommandTemperature.abbr:
                commands.set_temperature(device, payload)
            elif cmnd == CommandStatus.abbr:
                commands.update_stats(device)
            elif cmnd == CommandReboot.abbr:
                commands.reboot_device(device)
        except KeyError:
            pass
        except ValueError:
            pass

    def publish(self,
                topic,
                payload,
                qos=int(config['mqtt'].get('qos', 0)),
                retain=config['mqtt'].getboolean('retain', False)
                ):
        self.client.publish(topic, payload, qos, retain)

    def publish_json(self,
                     topic,
                     payload,
                     qos=int(config['mqtt'].get('qos', 0)),
                     retain=config['mqtt'].getboolean('retain', False)
                     ):
        self.publish(topic, json.dumps(payload), qos, retain)

    def run(self):
        self.client.connect(config['mqtt'].get('host'), int(config['mqtt'].get('port')), 60)
        self.client.loop_forever()

    def shutdown(self):
        self.client.loop_stop()
        self.client.disconnect()
        print('MQTT connection closed')
        sys.stdout.flush()


mqtt = MQTT()
