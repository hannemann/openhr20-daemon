from datetime import datetime
from SerialIO import serialIO


def time():
    d = datetime.now()
    return 'H{:02x}{:02x}{:02x}{:02x}'.format(d.hour, d.minute, d.second, round(d.microsecond / 10000))


def date():
    d = datetime.now()
    return 'Y{:02x}{:02x}{:02x}'.format(d.year - 2000, d.month, d.day)


def write():
    serialIO.write(date())
    serialIO.write(time())
