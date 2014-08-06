import os
import yaml
data = yaml.load(open('config.yaml', 'r'))

mesos_master_host = data['mesos_master_host']
print 'starting Theseus on this machine...'
os.system('docker run -d -p 22000:22 -p 5000:5001 -e MARATHON_HOST='+mesos_master_host+' -e MARATHON_PORT=8080 -e ETCD_HOST_ADDRESS='+marathon_master_host+' 54.189.193.228:5000/theseus')
print 'started!'