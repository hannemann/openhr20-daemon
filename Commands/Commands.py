import sys

from SerialIO import serialIO
from Devices import devices


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
            print('Command %s already buffered. Discarding new command...' % buffered_command.command)
            sys.stdout.flush()
        else:
            self.buffer[addr].append(command)

        devices.set_stat(addr, 'synced', False)

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
            print(' %s' % '(' + devices.get_name(addr) + ')' if devices.get_name(addr) is not None else '')

    def remove_from_buffer(self, addr):
        if self.has_command(addr):
            self.buffer[addr] = sorted(self.buffer[addr], key=lambda k: k.sent)
            for cmnd in self.buffer[addr]:
                if cmnd.sent > 0:
                    self.buffer[addr].remove(cmnd)
                    break

            if len(self.buffer) < 1:
                del self.buffer[addr]

    def discard_all(self, addr):
        if self.has_command(addr):
            del self.buffer[addr]

    def has_command(self, addr):
        result = addr in self.buffer and len(self.buffer[addr]) > 0
        devices.set_stat(addr, 'synced', not result)
        return result

    def test(self, command):
        self.buffer[0] = command


commands = Commands()
