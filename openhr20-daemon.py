#!/usr/bin/env python3

from OpenHR20 import OpenHR20
from MQTT import MQTT
import _thread


if __name__ == "__main__":
    openhr20 = OpenHR20()
    mqtt = MQTT()

    openhr20.start()
    mqtt.start()
