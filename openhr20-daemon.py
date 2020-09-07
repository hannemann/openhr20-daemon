#!/usr/bin/env python3

from OpenHR20 import openhr20
from MQTT import mqtt
import sys
import signal
from SerialIO import serialIO
from Httpd import httpd


def signal_handler(sig, frame):
    openhr20.shutdown()
    serialIO.shutdown()
    mqtt.shutdown()
    httpd.shutdown()
    sys.stderr.close()
    print("All threads stopped... exiting")
    sys.stdout.flush()
    sys.exit(0)


if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal_handler)

    serialIO.connected.wait(5)

    if serialIO.ser:
        mqtt.start()
        httpd.start()
        openhr20.start()
        mqtt.join()
        httpd.join()
        openhr20.join()
    else:
        sys.exit(1)
