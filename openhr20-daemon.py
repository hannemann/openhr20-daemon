#!/usr/bin/env python3

from OpenHR20 import OpenHR20
from MQTT import mqtt


if __name__ == "__main__":

    openhr20 = OpenHR20()
    try:

        openhr20.start()
        mqtt.start()
    except KeyboardInterrupt:
        openhr20.shutdown()

