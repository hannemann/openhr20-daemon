import ConfigParser, os

config = ConfigParser.ConfigParser()

for loc in os.curdir, os.path.expanduser("~/.config"), "/etc/openhr20", os.environ.get("OPENHR20_CONF"):
    try:
        if (loc is not None):
            with open(os.path.join(loc,"daemon.ini")) as source:
                config.readfp(source)
    except IOError:
        pass