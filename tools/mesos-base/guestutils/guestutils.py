import os
import etcd
import docker
import ast
import time
import socket
import etcd_driver
from sets import Set
# TODO replace hardcoded address

"""
assumes that these env variables are passed into container.
SERVICE_NAME: the friendly name of the service the container is an instance of. Note that it is possible to have multiple clusters of the same kind of application by giving them distinct friendly names.
CONTAINER_NAME: the friendly name of the instance, which is also used as the name of the container itself. This will also be the visible hostname from inside the container.
CONTAINER_HOST_ADDRESS: the external IP address of the host of the container. This can be used as the "advertised" address when services use dynamic service discovery techniques.
"""

#
# Wait for etcd config
#

def get_environment_name():
	# returns the name of the environment as defined in the description file. Could be useful to namespace information inside ZooKeeper for example.
	return 'default'
def get_service_name():
	# returns the friendly name of the service the container is a member of.
	return os.environ['SERVICE_NAME']
def get_container_name():
	# returns the friendly name of the container itself.
	return os.environ['CONTAINER_NAME']
def get_container_host_address():
	# returns the IP address or hostname of the host of the container. Useful if your application needs to advertise itself to some service discovery system.
	return os.environ['CONTAINER_HOST_ADDRESS']

def get_container_internal_address():
	# returns the IP address assigned to the container itself by Docker (its private IP address).
	return socket.gethostbyname(socket.gethostname())

def get_port(name, default = 'default_port'):
	# will return the exposed (internal) port number of a given named port for the current container instance. This is useful to set configuration parameters for example.
	# 'port_mapping': {'rpc': {'external': ('0.0.0.0', '9160/tcp'), 'exposed': '9160/tcp'}, 'storage': {'external': ('0.0.0.0', '7000/tcp'), 'exposed': '7000/tcp'}
	if default != 'default_port':
		return get_specific_exposed_port(get_service_name(), get_container_name(), name, default)
	return get_specific_exposed_port(get_service_name(), get_container_name(), name)

def get_node_list(service_name, ports=[], minimum=1, labels = []):
	# It takes in a service name and an optional list of port names and returns the list of IP addresses/hostname of the containers of that service. For each port specified, in order, it will append :<port number> to each host with the external port number. For example, if you want to return the list of ZooKeeper endpoints with their client ports:
	# get_node_list('zookeeper', ports=['client']) -> ['c414.ore1.domain.com:2181', 'c415.ore1.domain.com:2181']
	nodes = []
	service_groups = etcd_driver.get_service_groups(service_name)	
	for group in service_groups:
		try:
			group_labels = ast.literal_eval(group)
			fits_label_query = Set(labels).issubset(Set(group_labels))
			if fits_label_query:
				group_containers = etcd_driver.get_group_container_names(service_name, group)
				for container_name in group_containers:
					container_info = etcd_driver.get_container_info(service_name, group, container_name)
					host = str(container_info['instance_host'])
					portlist = ""
					for port in ports:
						p = get_specific_port(container_info['service_name'], container_info['instance_name'], port)
						p = ":" + p
						portlist = portlist + p
					nodes.append(str(host + portlist))
		except Exception as failure:
			# print 'getting group labels failed '+str(failure)
			print 'failed'
			print failure
	return nodes
def get_specific_host(service, container):
	# which can be used to return the hostname or IP address of a specific container from a given service, and
	container_encoded_labels = str(sorted(decode_marathon_id(container)['labels']))
	container_info = etcd_driver.get_container_info(service, container_encoded_labels, container)
	return container_info['instance_host']
def get_specific_port(service, container, port, default='default'):
	# to retrieve the external port number of a specific named port of a given container.
	container_encoded_labels = str(sorted(decode_marathon_id(container)['labels']))
	container_info = etcd_driver.get_container_info(service, container_encoded_labels, container)
	port_mappings = container_info['port_mapping']
	port_mapping = port_mappings.get(port)
	if port_mapping is None:
		return default
	return port_mapping['external'][1].replace('/tcp', '')

def get_specific_exposed_port(service, container, port, default='default'):
	# to retrieve the exposed (internal) port number of a specific named port of a given container.

	container_encoded_labels = str(sorted(decode_marathon_id(container)['labels']))
	container_info = etcd_driver.get_container_info(service, container_encoded_labels, container)
	port_mappings = container_info['port_mapping']
	port_mapping = port_mappings.get(port)
	if port_mapping is None:
		return default
	return port_mapping['exposed'].replace('/tcp', '')


def decode_marathon_id(marathon_id, id_separator = 'D.L'):
    # split up id
    id_split = marathon_id.split(id_separator)
    service_name = str(id_split[0])
    labels = ast.literal_eval('['+id_split[1].replace("-", "'").replace(".", ",")+']')
    version = str(id_split[2])
    return {'service':service_name, 'labels':labels, 'version':version}

def small_test():
	# print client.read("/services").children
	# print etcd_driver.get_service_names()
	# print etcd_driver.get_service_containers('ingestor')
	labels = ['testing']
	service_name = 'ingestor'
	ports = ['ssh']

	nodes = get_node_list(service_name, ports, labels=labels)
	print nodes
	print get_port('ssh')
	# print get_port('ssh')
# small_test()
def test_all():
	try:
		print 'get_environment_name():'
		print get_environment_name()
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

	try:
		print 'get_service_name():'
		print get_service_name()
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

	try:
		print 'get_container_name():'
		print get_container_name()
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

	try:
		print 'get_container_host_address():'
		print get_container_host_address()
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

	try:
		print 'get_container_internal_address():'
		print get_container_internal_address()
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

	try:
		print 'get_port(name, default = default_port):'
		print get_port('ssh', 1234)
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

	try:
		print 'get_node_list(service, ports=[], minimum=1):'
		print get_node_list('ingestor', ports = ['ssh'])
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'
	try:
		print 'get_specific_host(service, container):'
		print get_specific_host('ingestor', get_container_name())
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

	try:
		print 'get_specific_port(service, container, port, default'
		print get_specific_port('ingestor', get_container_name(), 'ssh', 1234)
		print get_specific_port('ingestor', get_container_name(), 'ssh')
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

	try:
		print 'get_specific_exposed_port(service, container, port, defaul'
		print get_specific_exposed_port('ingestor', get_container_name(), 'ssh', 1234)
		print get_specific_exposed_port('ingestor', get_container_name(), 'ssh')
	except Exception, e:
		print e.__doc__
		print e.message
		print 'failed'

# test_all()
# small_test()