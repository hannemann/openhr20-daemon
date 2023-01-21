#!/usr/bin/env python3
import __init__ as daemon
import sys
import signal


def signal_handler(sig, frame):
    daemon.openhr20.shutdown()
    daemon.ws.shutdown()
    daemon.serialIO.shutdown()
    daemon.mqtt.shutdown()
    daemon.httpd.shutdown()
    sys.stderr.close()
    print("All threads stopped... exiting")
    sys.stdout.flush()
    sys.exit(0)


if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal_handler)

    daemon.serialIO.connected.wait(5)

    if daemon.serialIO.ser:
        daemon.mqtt.start()
        daemon.httpd.start()
        daemon.ws.start()
        daemon.openhr20.start()
        daemon.mqtt.join()
        daemon.httpd.join()
        daemon.ws.join()
        daemon.openhr20.join()
    else:
        sys.exit(1)
