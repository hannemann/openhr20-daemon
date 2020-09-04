from SerialIO import serialIO

class Commands:

    buffer = {}

    def add(self, addr, command):
        if addr not in self.buffer:
            self.buffer[addr] = []

        self.buffer[addr].append(command)
        print(self.sorted_by_commands_count())

    def sorted_by_commands_count(self):
        return sorted(self.buffer, key=lambda k: len(self.buffer[k]), reverse=True)

    def send(self, addr):
        print('Send commands to device %d' % addr)
        weight = 0
        bank = 0
        q = ''
        if addr in self.buffer:
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

    def weights(self, cmnd):
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

    def test(self, command):
        self.buffer[0] = command


commands = Commands()
