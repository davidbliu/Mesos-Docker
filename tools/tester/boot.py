import os
import time

print 'hi my name is david'
os.system('printenv')
import guestutils
time.sleep(5)
guestutils.test_all()

os.system("/usr/sbin/sshd -D")