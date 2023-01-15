from datetime import datetime
import pytz
import os
from SerialIO import serialIO

tz = pytz.timezone(os.getenv('TZ'))


def hex_time():
    d = datetime.now(tz)
    return 'H{:02x}{:02x}{:02x}{:02x}'.format(d.hour, d.minute, d.second, round(d.microsecond / 10000))


def hex_date():
    d = datetime.now(tz)
    return 'Y{:02x}{:02x}{:02x}'.format(d.year - 2000, d.month, d.day)


def write():
    serialIO.write(hex_date())
    serialIO.write(hex_time())
