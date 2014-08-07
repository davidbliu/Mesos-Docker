import os


os.system('printenv')
print '<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'
print 'starting sshd'

os.system("/usr/sbin/sshd -D")