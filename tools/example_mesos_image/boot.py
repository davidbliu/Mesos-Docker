import os, sys
import time
import subprocess
sys.path.append('/opt/example/guestutils')
#
# import from guestutils
# gives access too all guestutils functions (these have the same method signatures as the familiar maestro guestutils)
#
import guestutils
#
# start watcher
# container will now recieve events when services that it is watching are changed
# it will use the user-defined watch_methods to respond to those changes
#
subprocess.Popen(["python", '-u', "/opt/example/guestutils/watcher.py"])
while True:
	time.sleep(60)