import json
import sys
import os
import paho.mqtt.client as mqttc
import threading
from Commands.CommandTemperature import CommandTemperature
from Commands.CommandMode import CommandMode
from Commands.CommandStatus import CommandStatus
from Commands.CommandReboot import CommandReboot
from Devices import devices

mqtt_qos = int(os.getenv("MQTT_QOS"))
mqtt_retain = os.getenv("MQTT_RETAIN") == 'True'


class MQTT(threading.Thread):
    daemon = True
    count = 0
    temp = 'temp'
    cmnd_topic = os.getenv("MQTT_CMND_TOPIC")
    stats_topic = os.getenv("MQTT_STATS_TOPIC")
    availability_topic = os.getenv("MQTT_AVAILABILITY_TOPIC")
    host = os.getenv("MQTT_HOST")
    port = int(os.getenv("MQTT_PORT"))
    debug = os.getenv('MQTT_DEBUG') == 'True'
    qos = mqtt_qos
    retain = mqtt_retain

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
        cmnd_topic = self.cmnd_topic.strip('/') + "/#"
        self.client.subscribe(cmnd_topic)
        print('MQTT: Subscribed to topic {}'.format(cmnd_topic))
        sys.stdout.flush()

    def on_message(self, client, userdata, msg):
        topic = msg.topic.replace(self.cmnd_topic.strip('/') + '/', '').split('/')
        cmnd = topic[0]
        addr = int(topic[1], 10)
        if self.debug:
            print(" < MQTT: {} {} {}".format(addr, cmnd, msg.payload.decode('utf_8').strip()))
            sys.stdout.flush()

        try:
            payload = msg.payload.decode('utf_8').strip()
            device = devices.get_device(addr)
            if cmnd == CommandMode.abbr:
                try:
                    payload = json.loads(os.getenv("MQTT_MODES_RECEIVE"))[payload]
                except KeyError:
                    pass
                device.set_mode(payload)
                if device.group is not None:
                    for dev in device.group.devices:
                        self.publish_availability(dev)

            elif cmnd == CommandTemperature.abbr:
                device.set_temperature(payload)
                if device.group is not None:
                    for dev in device.group.devices:
                        self.publish_availability(dev)

            elif cmnd == CommandStatus.abbr:
                device.update_stats()
                self.publish_availability(device)

            elif cmnd == CommandReboot.abbr:
                device.reboot_device()
                self.publish_availability(device)

            elif cmnd == 'preset':
                try:
                    payload = json.loads(os.getenv("MQTT_PRESETS_RECEIVE"))[payload]
                except KeyError:
                    pass
                device.set_preset(payload)
                if device.group is not None:
                    for dev in device.group.devices:
                        self.publish_availability(dev)

        except KeyError:
            pass
        except ValueError:
            pass

    def publish(self, topic, payload, qos=mqtt_qos, retain=mqtt_retain):
        self.client.publish(topic, payload, qos, retain)
        if self.debug:
            print(" > MQTT: {} {} (QOS {}, Retain {})".format(topic, payload, qos, retain))
        else:
            print(" > MQTT: {}".format(topic))
        sys.stdout.flush()

    def publish_json(self, topic, payload, qos=mqtt_qos, retain=mqtt_retain):
        self.publish(topic, json.dumps(payload), qos, retain)

    def publish_stats(self, device):
        stats = device.dict()
        try:
            stats['mode'] = json.loads(os.getenv("MQTT_MODES_PUBLISH"))[stats['mode']]
        except KeyError:
            pass
        try:
            stats['preset'] = json.loads(os.getenv("MQTT_PRESETS_PUBLISH"))[stats['preset']]
        except KeyError:
            pass
        self.publish(self.stats_topic.strip('/') + '/{}'.format(device.addr), json.dumps(stats))

    def publish_availability(self, device):
        topic = self.availability_topic.strip('/') + '/{}'.format(device.addr)
        payload = 'offline' if device.available == device.AVAILABLE_OFFLINE or device.synced is False else 'online'
        mqtt.publish(topic, payload)

    def run(self):
        print('MQTT: Connect to broker {}:{}'.format(self.host, self.port))
        self.client.connect(self.host, self.port, 60)
        self.client.loop_forever()

    def shutdown(self):
        self.client.loop_stop()
        self.client.disconnect()
        print('MQTT connection closed')
        sys.stdout.flush()


mqtt = MQTT()
