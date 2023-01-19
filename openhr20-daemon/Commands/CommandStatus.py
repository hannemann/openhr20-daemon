from Commands.AbstractCommand import AbstractCommand


class CommandStatus(AbstractCommand):

    abbr = 'status'
    sent = 0
    command = 'D'
    weight = 10
