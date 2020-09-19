import json
import sys
import paho.mqtt.client as mqttc
import threading
from Commands.CommandTemperature import CommandTemperature
from Commands.CommandMode import CommandMode
from Commands.CommandStatus import CommandStatus
from Commands.CommandReboot import CommandReboot
from Config import config, defaults
from Devices import devices


class MQTT(threading.Thread):
    daemon = True
    count = 0
    temp = 'temp'
    cmnd_topic = config.get('mqtt', 'cmnd_topic', fallback=defaults['mqtt']['cmnd_topic'])
    stats_topic = config.get('mqtt', 'stats_topic', fallback=defaults['mqtt']['stats_topic'])
    host = config.get('mqtt', 'host', fallback=defaults['mqtt']['host'])
    port = config.getint('mqtt', 'port', fallback=defaults['mqtt']['port'])
    qos = config.getint('mqtt', 'qos', fallback=defaults['mqtt']['qos'])
    retain = config.getboolean('mqtt', 'retain', fallback=defaults['mqtt']['retain'])

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
        print('MQTT: Subscribed to topic %s' % cmnd_topic)
        sys.stdout.flush()

    def on_message(self, client, userdata, msg):
        topic = msg.topic.replace(self.cmnd_topic.strip('/') + '/', '').split('/')
        cmnd = topic[0]
        addr = int(topic[1], 10)
        print("MQTT: %d %s %s" % (addr, cmnd, msg.payload.decode('utf_8').strip()))
        sys.stdout.flush()

        try:
            payload = msg.payload.decode('utf_8').strip()
            device = devices.get_device(addr)
            if cmnd == CommandMode.abbr:
                mapped_mode = config.get('mqtt-modes-receive', payload, fallback=False)
                if mapped_mode is not False:
                    payload = mapped_mode
                device.set_mode(payload)

            elif cmnd == CommandTemperature.abbr:
                device.set_temperature(payload)

            elif cmnd == CommandStatus.abbr:
                device.update_stats()

            elif cmnd == CommandReboot.abbr:
                device.reboot_device()

            elif cmnd == 'preset':
                mapped_preset = config.get('mqtt-presets-receive', payload, fallback=False)
                if mapped_preset is not False:
                    payload = mapped_preset
                device.set_preset(payload)

        except KeyError:
            pass
        except ValueError:
            pass

    def publish(self,
                topic,
                payload,
                qos=config.getint('mqtt', 'qos', fallback=defaults['mqtt']['qos']),
                retain=config.getboolean('mqtt', 'retain', fallback=defaults['mqtt']['retain'])
                ):
        self.client.publish(topic, payload, qos, retain)

    def publish_json(self,
                     topic,
                     payload,
                     qos=config.getint('mqtt', 'qos', fallback=defaults['mqtt']['qos']),
                     retain=config.getboolean('mqtt', 'retain', fallback=defaults['mqtt']['retain'])
                     ):
        self.publish(topic, json.dumps(payload), qos, retain)

    def publish_stats(self, device):
        stats = device.get_stats()
        mapped_mode = config.get('mqtt-modes-publish', stats['mode'], fallback=False)
        if mapped_mode is not False:
            stats['mode'] = mapped_mode
        mapped_preset = config.get('mqtt-presets-publish', stats['preset'], fallback=False)
        if mapped_preset is not False:
            stats['preset'] = mapped_preset
        self.publish(self.stats_topic.strip('/') + '/%d' % device.addr, json.dumps(stats))

    @staticmethod
    def publish_availability(device):
        topic = config.get(
            'mqtt', 'availability_topic', fallback='stat/openhr20/AVAILABLE/').strip('/') + '/%d' % device.addr
        mqtt.publish(topic, 'offline' if device.available == device.AVAILABLE_OFFLINE else 'online')

    def run(self):
        self.client.connect(self.host, self.port, 60)
        self.client.loop_forever()

    def shutdown(self):
        self.client.loop_stop()
        self.client.disconnect()
        print('MQTT connection closed')
        sys.stdout.flush()


mqtt = MQTT()
