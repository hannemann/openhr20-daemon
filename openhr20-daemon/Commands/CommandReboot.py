from Commands.AbstractCommand import AbstractCommand


class CommandReboot(AbstractCommand):

    abbr = 'reboot'
    sent = 0
    command = 'B1324'
    weight = 10
