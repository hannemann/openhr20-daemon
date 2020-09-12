import sys

from SerialIO import serialIO
from Devices import devices, set_synced


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

        buffered_command = next((x for x in self.buffer[addr] if x.command == command.command), None)
        if buffered_command is not None:
            print('Command %s already buffered' % buffered_command.command)
            sys.stdout.flush()
            buffered_command.sent += 1
        else:
            self.buffer[addr].append(command)

        set_synced(addr, False)

    def send(self, addr):
        weight = 0
        bank = 0
        q = []
        i = 0
        if self.has_command(addr):
            for cmnd in self.buffer[addr]:
                cw = cmnd.weight
                weight += cw
                if weight > 10:
                    if ++bank > 7:
                        break
                    weight = cw
                r = "(%02x-%x)%s" % (addr, bank, cmnd.command)
                q.append(r)
                cmnd.sent += 1
                i += 1
                if i > 25:
                    break
            serialIO.write('\n'.join(q), '')
            print(' %s' % '(' + devices['names'][str(addr)] + ')' if str(addr) in devices['names'] else '')

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
        result = addr in self.buffer and len(self.buffer[addr]) > 0
        set_synced(addr, not result)
        return result

    def test(self, command):
        self.buffer[0] = command


commands = Commands()
