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
### Init configuration
Run the daemon once as root and the config file will be created: /etc/openhr20/daemon.conf  
Adjust to your needs

Install the systemd service file
```bash
systemctl start openhr20-python-daemon
```
Maybe you want to adjust the path since it currently points to /usr/local/bin/  

Enable and start the daemon
```bash
sudo systemctl enable openhr20-python-daemon
sudo systemctl start openhr20-python-daemon
```

#### Notes
