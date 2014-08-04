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

### Layers
* workstation
  * developer provides declarative configuration for applications
  * environment variables, ports, labels, constraints, image name, instances, cpu, mem, etc
* marathon framework (theseus)
  * organizes and manages services deployed (what is deployed where, what ports, what configuration, etc)
  * allow user to see what is deployed, can filter by labels (like cassandra testing)
  * basic container metrics and logs are collected in one place
  * basic scheduling routines: rolling restart service with configurable wait time, constraints for which hosts to deploy onto, etc
* mesos master and marathon
  * recieves apps and tasks from theseus and ensures they remain running
  * publish information to subscriber -> etcd
* mesos-slave machine
  * makes resource offers, recieves tasks from mesos master, executes them
  * basic logging and metrics for containers running on it 
  * should be a "container-optimized machine". it is configured to run containers -> and monitor them and report how they are doing
* deimos and docker
  * run the container
  * containers recieve topology from etcd
  * containers watch etcd for updates

__application configuration:__ interfaces with cluster manager. what and how many to deploy. some constraints like deploy only on large vms and all containers on unique hosts etc

__cluster manager:__ know what is deployed where, can monitor slaves, resources and performance aware (knows what resources are
available and what services/containers are stressed

__slave node:__ know about processes running on itself, monitor cpu memory network etc, logs -> ship to cluster manager

__application:__ only needs to care about itself (what to do with endpoints of other services, 
what to do when endpoints of other services change, how to shut down gracefully (ex when sigterm sent to it etc))


### Alternate design choices
* who updates configuration in etcd?
 * current: subscriber to marathon
 * process running on slave to check
 * container
* who records metrics
 * current: container
 * process running on slave
* who holds logs/debug information
 * current: container
 * process running on slave
* who holds record of what commands given to management framework (container config etc)?
 * current: container management framework
 * etcd (could have a directory for config and a directory for enpoint info)
