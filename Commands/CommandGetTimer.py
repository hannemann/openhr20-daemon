from Commands.AbstractCommand import AbstractCommand


class CommandGetTimer(AbstractCommand):

    abbr = 'get_timer'
    sent = 0
    command = 'R'
    weight = 2

    def __init__(self, day, slot):
        self.command = '{}{}{}'.format(self.command, day, slot)

    @staticmethod
    def valid(day, slot):
        return 0 <= day <= 7 and 0 <= slot <= 7
