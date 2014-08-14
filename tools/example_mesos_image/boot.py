import os
import time
import subprocess


#
# start watcher
#
subprocess.Popen(["python", '-u', "/opt/example/guestutils/watcher.py"])
while True:
	time.sleep(60)