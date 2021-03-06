#
# we want watcher to startup only after container starts up, so wait for that to happen
#
import os
import time
while True:
	if os.environ.get('CONTAINER_HOST_ADDRESS') is None:
		print 'container not started yet'
		time.sleep(60)
	else:
		break


import etcd
import ast
import threading
import sys
import etcd_driver

etcd_host_address = os.environ['ETCD_HOST_ADDRESS'] 
client = etcd.Client(host=etcd_host_address, port=4001, read_timeout = sys.maxint)


#
# watches key in etcd, gets delta
# TODO doesn't support watching labels. ingestor label=[testing] doesn't work
#
# 
def watch_etcd_key(service, labels=[]):
	
	watch_key = '/services/'+str(service)
	#
	# store previous value 
	#'
	prev_containers = etcd_driver.get_service_containers(service)
	previous_value = len(prev_containers)
	print 'previous value was '+str(previous_value)
	current_value = previous_value
	curr_containers = prev_containers
	print 'started watching key '+ watch_key
	while True:
		event = client.read(watch_key, recursive=True, wait=True, timeout=0)
			#
			# number of nodes has changed...
			#
		print 'watch key has changed>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
		current_containers = etcd_driver.get_service_containers(service)
		curr = len(current_containers)
		previous_value = current_value
		current_value = curr
		prev_containers = curr_containers
		curr_containers = current_containers
		delta = current_value - previous_value
		service_change(watch_key, delta)
		print 'watching for next change...<<<<<<<<<<<<<<<<<<<<<<<<'
			
#
# user defined function, pluggable
# what procedure to invoke when services you depend on change
# import watch methods here so they are modified based on user-submitted watch methods
#
def service_change(service, delta):
	try:
		import watch_methods 
		print 'running custom watch method'
		watch_methods.service_change(service, delta)
	except:
		print 'not implemented yet. service was '+str(service)+', delta was '+str(delta)


class ThreadClass(threading.Thread):
	service = None
	def set_service(self, service):
		self.service = service
	def run(self):
		service = self.service
		watch_etcd_key(service)


#
# spawns multiple threads to watch multiple keys
# TODO: think of cleaner/efficient-er way to do this
#
def watch_keys(service_list):
	for service in service_list:
		t=ThreadClass()
		t.set_service(service)
		t.daemon=True
		t.start()

def startup_watcher():
	

	keys = os.environ.get('WATCHES')
	
	if keys:
		my_keys = keys.split(',')
		print 'starting to watch '+str(my_keys)
		watch_keys(my_keys)
		#
		# Main process: keep threads alive
		#
		while True:
			time.sleep(60)
	else:
		print 'environment variable WATCHES not set, not watching anything...'


startup_watcher()