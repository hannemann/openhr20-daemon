#!/usr/bin/env python3

from OpenHR20 import OpenHR20
from MQTT import mqtt
import sys
import signal
from SerialIO import serialIO
from httpd.BottleHttp import run_http

openhr20 = OpenHR20()


def signal_handler(sig, frame):
    openhr20.shutdown()
    serialIO.shutdown()
    mqtt.shutdown()
    print("All threads stopped... exiting")
    sys.stdout.flush()
    sys.exit(0)


if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal_handler)

    serialIO.connected.wait(5)

    if serialIO.ser:
        mqtt.start()
        openhr20.start()
        run_http()
        mqtt.join()
        openhr20.join()
    else:
        sys.exit(1)
