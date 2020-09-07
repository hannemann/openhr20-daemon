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
### Rasbian (Stretch)
```bash
pip3 install paho-mqtt
sudo apt install python3-bottle
```
```
git clone https://github.com/hannemann/openhr20-daemon.git
```
## Prerequisites

Install the systemd service file
```bash
mkdir /etc/openhr20
mkdir/var/cache/openhr20
systemctl start openhr20-python-daemon
```
### Init configuration
Adjust the path to the main python file openhr20-daemon.py since it currently points to /usr/local/bin/  
Run the daemon once as root to create the config and devices files:
* /etc/openhr20/daemon.conf
* /var/cache/openhr20  
Adjust to your needs

Enable and start the daemon
```bash
sudo systemctl enable openhr20-python-daemon
sudo systemctl start openhr20-python-daemon
```

#### Notes
