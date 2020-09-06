# Daemon for the OpenHR20 Master

Goals:
* mimic the original php daemon
* subscribe to mqtt instead of using an sqlite3 database
* publish status messages via mqtt
* Stats can be stored and processed by e.g. Homeassistant
* no need to lock a frontend

## Installation
### Ubuntu:
```bash
sudo apt install python3-paho-mqtt python3-bottle
```
Install the systemd service file (tbd)
```bash
systemctl start openhr20
```
#### Notes
Before start invoke
```bash
stty -F /dev/ttyUSB0 38400
```