from Commands.AbstractCommand import AbstractCommand


class CommandSetTimer(AbstractCommand):

    abbr = 'set_timer'
    sent = 0
    command = 'W'
    weight = 4

    def __init__(self, day, value):
        self.command = '%s%s%s' % (self.command, day, value)

    @staticmethod
    def valid(day, value):
        return 0 <= int(day[0]) <= 7 \
               and 0 <= int(day[1]) <= 7 \
               and 0 <= int(value[0]) <= 3 \
               and (0 <= int(value[1:], 16) <= 24 * 60 or int(value[1:], 16) == int('fff', 16))
