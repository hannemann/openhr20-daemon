#!/usr/bin/env python

import os, sys
import pwd, grp
import time
import signal
import daemon, lockfile
from config import config

uid = pwd.getpwnam('nobody').pw_uid
gid = grp.getgrnam('nogroup').gr_gid

print('User: %s' % uid)
print('Group: %s' % gid)

class Openhr20(object):

        stdin_path = "/dev/null"
        stdout_path = "/tmp/openhr20.out"
        stderr_path =  "/tmp/openhr20.err"
        pidfile_path =  "/var/run/openhr20-daemon.pid"
        pidfile_timeout = 3
        terminate = False
        
        def __init__(self):
            print('Initialized')

        def action(self, i):
            print("Iteration %d" % i)

        def run(self):
            print('OpenHR20 Python Daemon')
            fd = open('/dev/ttyACM0', 'w')
            for line in fd.readline(256):
                self.action(line)
                print('===========')
                
                if self.terminate:
                    break
                
            print('Terminated')
            sys.exit(0)                
                    
        def shutdown(self, a, b):
            print('Catched SIGTERM')
            self.terminate = True

if __name__ == "__main__":
    
    openhr20 = Openhr20()
    
    context = daemon.DaemonContext(
        working_directory='/tmp',
        umask=0x002,
        pidfile=lockfile.FileLock(openhr20.pidfile_path),
    )
        
    context.signal_map = {
        signal.SIGTERM: openhr20.shutdown
    }    
    
    context.stdout = open(openhr20.stdout_path, 'w+')
    context.stderr = open(openhr20.stderr_path, 'w+', buffering=0)
    
    with context:
        openhr20.run()