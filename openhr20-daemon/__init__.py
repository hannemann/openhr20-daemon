import OpenHR20
import MQTT
import WebSocket
import Httpd
import SerialIO
from httpd.Controllers.PageController import PageController
from httpd.Controllers.CommandsController import CommandsController
from httpd.Controllers.RemoteController import RemoteController
from httpd.Controllers.DeviceController import DeviceController
import Devices
import Device
import Group
import WebsocketCommands

Device = Device.Device
Group = Group.Group
WebsocketCommands = WebsocketCommands.WebsocketCommands

serialIO = SerialIO.SerialIO()
openhr20 = OpenHR20.OpenHR20()
devices = Devices.Devices()
mqtt = MQTT.MQTT()
ws = WebSocket.WebSocket()
httpd = Httpd.Httpd()
pageController = PageController(Httpd.httpd_path)
commandsController = CommandsController()
remoteController = RemoteController()
deviceController = DeviceController()