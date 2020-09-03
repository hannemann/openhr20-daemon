

class Commands:

    buffer = []

    def push(self, command):
        self.buffer.append(command)

    def test(self, command):
        self.buffer[0] = command


commands = Commands()
