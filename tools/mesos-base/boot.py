# scp -r user@remote:src_directory dst_directory

import os

os.system('sudo nsenter --target $PID --mount --uts --ipc --net --pid')
os.system('ls')