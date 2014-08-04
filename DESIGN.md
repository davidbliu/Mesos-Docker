# Architecture

<img src='/comparisons/mesos-kub.png'></img>

# Concepts

* __services__ like haproxy, ingestor, cassandra, etc..
* __labeled groups__ identified by belonging to a __service__ and having a unique set of labels 
	* ex: ['dev','frontend'] 

# Service Discovery

### etcd directory structure

__paths__
* /services
	* contains all services
* /services/{{service_name}}
	* root directory for a given service
* /services/{{service_name}}/{{labeled_group}}
	* root directory for a labeled group
* /services/{{service_name}}/{{labeled_group}}/config
	* configuration parameters given to this labeled group when deployed
* /services/{{service_name}}/{{labeled_group}}/containers
	* root directory for containers
* /services/{{service_name}}/{{labeled_group}}/containers/{{container_name}}
	* root directory for specific container
* /services/{{service_name}}/{{labeled_group}}/containers/{{container_name}}/info
	* value containers instance_host, instance_port, port_mappings, and instance_name	

__etcd driver__
an interface to etcd, has methods to store and retrieve information from etcd
* create_service(service_name):
* create_group(service_name, encoded_labels, config):
* remove_service(service_name):
* remove_group(service_name, encoded_labels):
* service_exists(service_name):
* group_exists(service_name, encoded_labels):
* get_service_names():
* get_service_groups(service_name):
* get_service_containers(service_name):
* get_group_config(service_name, encoded_labels):
* set_group_config(service_name, encoded_labels, config):
* get_group_container_names(service_name, encoded_labels):
* container_exists(service_name, encoded_labels, container_name):
* get_container_info(service_name, encoded_labels, container_name):
* set_container_info(service_name, encoded_labels, container_name, info):
* register_container(service_name, encoded_labels, container_name, info):
* deregister_container(service_name, encoded_labels, container_name):

# Theseus (container management framework)

Theseus is a command line client that allows you to create, update, and remove groups. 
it handles namespacing and generic scheduling processes like rolling updates.
It also has a viewer.

# Theory
