import sys
from SerialIO import serialIO


class Commands:

    buffer = {}

    def add(self, device, command):
        addr = device.addr
        if addr not in self.buffer:
            self.buffer[addr] = []

        buffered_command = next((x for x in self.buffer[addr] if x.command == command.command), None)
        if buffered_command is not None:
            print('Command %s already buffered. Discarding new command...' % buffered_command.command)
            sys.stdout.flush()
        else:
            self.buffer[addr].append(command)

        device.synced = False

    def send(self, device):
        weight = 0
        bank = 0
        q = []
        i = 0
        if self.has_command(device):
            for cmnd in self.buffer[device.addr]:
                cw = cmnd.weight
                weight += cw
                if weight > 10:
                    if ++bank > 7:
                        break
                    weight = cw
                r = "(%02x-%x)%s" % (device.addr, bank, cmnd.command)
                q.append(r)
                cmnd.sent += 1
                i += 1
                if i > 25:
                    break
            serialIO.write('\n'.join(q), '')
            print(' %s' % '(' + device.name + ')')

    def remove_from_buffer(self, device):
        if self.has_command(device):
            self.buffer[device.addr] = sorted(self.buffer[device.addr], key=lambda k: k.sent)
            for cmnd in self.buffer[device.addr]:
                if cmnd.sent > 0:
                    self.buffer[device.addr].remove(cmnd)
                    break

            if len(self.buffer[device.addr]) < 1:
                del self.buffer[device.addr]

    def discard_all(self, device):
        if self.has_command(device):
            del self.buffer[device.addr]

    def has_command(self, device):
        result = device.addr in self.buffer and len(self.buffer[device.addr]) > 0
        device.synced = not result
        return result

    def send_sync_package(self, line):
        req = [0, 0, 0, 0]
        v = 'O0000'
        pr = 0
        if len(self.buffer) > 0:
            for addr in sorted(self.buffer, key=lambda k: len(self.buffer[k]), reverse=True):
                v = None
                cmnds = self.buffer[addr]
                if line == 'N1?' and len(cmnds) > 10:
                    v = "O%02x%02x" % (addr, pr)
                    pr = addr
                else:
                    req[int(addr/8)] |= int(pow(2, addr % 8))

        if v is None:
            v = "P%02x%02x%02x%02x" % (req[0], req[1], req[2], req[3])

        serialIO.write(v)


commands = Commands()
