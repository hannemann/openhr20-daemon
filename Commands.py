from SerialIO import serialIO


def weights(cmnd):
    table = {
        'D': 10,
        'S': 4,
        'W': 4,
        'G': 2,
        'R': 2,
        'T': 2
    }

    if cmnd in table:
        return table[cmnd]
    else:
        return 10


class Commands:

    buffer = {}

    def add(self, addr, command):
        if addr not in self.buffer:
            self.buffer[addr] = []

        self.buffer[addr].append(command)

    def send(self, addr):
        weight = 0
        bank = 0
        q = ''
        if self.has_command(addr):
            for cmnd in self.buffer[addr]:
                cw = cmnd.weight
                weight += cw
                if weight > 10:
                    if ++bank > 7:
                        break
                    weight = cw
                r = "(%02x-%x)%s" % (addr, bank, cmnd.command)
                q += r
                serialIO.write(q)
                cmnd.sent += 1

    def remove_from_buffer(self, addr):
        if self.has_command(addr):
            buffer = self.buffer[addr]
            buffer = sorted(buffer, key=lambda k: k.sent)
            buffer.pop(0)
            if len(buffer) > 0:
                self.buffer[addr] = buffer
            else:
                del self.buffer[addr]

    def has_command(self, addr):
        return addr in self.buffer and len(self.buffer[addr]) > 0

    def test(self, command):
        self.buffer[0] = command


commands = Commands()
