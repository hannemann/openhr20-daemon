from Commands.AbstractCommand import AbstractCommand


class CommandTemperature(AbstractCommand):

    abbr = 'temp'
    sent = 0
    command = ''
    weight = 10

    def __init__(self, temperature):
        self.command = 'A{:02x}'.format(int(float(temperature)*2))

    @staticmethod
    def validate(temperature):
        if not 5 <= float(temperature) <= 30:
            raise ValueError
