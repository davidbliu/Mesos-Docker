import os
import time
import subprocess

print 'hi my name is david'
os.system('printenv')
import guestutils
time.sleep(5)
guestutils.test_all()

print 'starting watcher'
# import watcher
# watcher.start_watching()
subprocess.Popen(["python", '-u', "/opt/tester/watcher.py"])

print 'starting ssh'
os.system("/usr/sbin/sshd -D")