# Architecture

- [Service Discovery](#service-discovery)
	- [etcd directory structure](#etcd-directory-structure)
	- [etcd driver](#etcd-driver)
	- [subscriber](#subscriber)
	- [container level tools](#container-level-tools)
- [Theseus (container management layer)](#theseus)
- [Theory](#theory)
	- [layers](#layers)
	- [alternate design choices](#alternate-design-choices)

<img src='/comparisons/mesos-kub.png'></img>

# Concepts

* __services__ like `haproxy`, `ingestor`, `cassandra`, etc..
* __labeled groups__ identified by belonging to a __service__ and having a unique set of labels 
	* ex: `['dev','frontend']` 

# Service Discovery

### etcd directory structure

__paths__
* `/services`
	* contains all services
* `/services/{{service_name}}`
	* root directory for a given service
* `/services/{{service_name}}/{{labeled_group}}`
	* root directory for a labeled group
* `/services/{{service_name}}/{{labeled_group}}/config`
	* configuration parameters given to this labeled group when deployed
* `/services/{{service_name}}/{{labeled_group}}/containers`
	* root directory for containers
* `/services/{{service_name}}/{{labeled_group}}/containers/{{container_name}}`
	* root directory for specific container
* `/services/{{service_name}}/{{labeled_group}}/containers/{{container_name}}/info`
	* value containers instance_host, instance_port, port_mappings, and instance_name	

__etcd driver__
an interface to etcd, has methods to store and retrieve information from etcd
* `create_service(service_name)`
* `create_group(service_name, encoded_labels, config)`
* `remove_service(service_name)`
* `remove_group(service_name, encoded_labels)`
* `service_exists(service_name)`
* `group_exists(service_name, encoded_labels)`
* `get_service_names()`
* `get_service_groups(service_name)`
* `get_service_containers(service_name)`
* `get_group_config(service_name, encoded_labels)`
* `set_group_config(service_name, encoded_labels, config)`
* `get_group_container_names(service_name, encoded_labels)`
* `container_exists(service_name, encoded_labels, container_name)`
* `get_container_info(service_name, encoded_labels, container_name)`
* `set_container_info(service_name, encoded_labels, container_name, info)`
* `register_container(service_name, encoded_labels, container_name, info)`
* `deregister_container(service_name, encoded_labels, container_name)`

### Subscriber

a Marathon subscriber maintains configuration in etcd. This is done by interfacing with marathon's event bus. after running marathon
on your mesos master, setup the subscriber. the subscriber registers a callback url with marathon and then recieves events
when tasks are started or killed. from the marathon event, the subscriber updates etcd with what services and groups have containers
running and what hosts and ports they are run on

__in progress:__ the subscriber is currently coupled with marathon since it updates etcd configuration based on what marathon says is running.
a better architecture may be to place subscribers on each mesos slave to monitor the containers running on that slave and report configuration 
to etcd. This decouples the subscriber from marathon.

### Container-level tools

containers interface with the service discovery system with __guestutils__ and __watch_methods__. guestutils provides methods to pull configuration
information from etcd while watch_methods provides a way to write pluggable methods and recieve notifications pushed from etcd
when services change. 

__guestutils:__ see main README for guestutils methods

__watch_methods:__ see getting started section of main README for how to write pluggable methods.
watch_methods is called from within watcher.py, which recieves notifications from etcd via watching keys. containers can 
select which keys to watch through the `WATCHES` environment variable. `WATCHES` should be a comma-separated string of the 
services that you want to watch.


# Theseus

Theseus is a command line client that allows you to create, update, and remove groups. 
it handles namespacing and generic scheduling processes like rolling updates.
It also has a viewer.

__motivation for theseus:__ marathon is not the ideal container-friendly interface for deploying and organizing dockerized applications.
it has concepts of apps and tasks but doesn't explicitly support services and groups. Therefore, a lightweight framework on top of marathon
to handle these tasks provides a robust way to manage docker containers. Since marathon is in flux and will soon accommodate namespacing 
and even scheduling tasks like rolling updates, this framework is even more crucial. instead of changing how developers interface with marathon
you can simply update your framework (theseus) according to the changes in marathon. this allows you to keep the interface
to your cluster the same even with changes to marathon.

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
