# Demos

### Sprint 1 Demo (old)
* mesos master/slaves/marathon already running on ec2 instances
 * mesos: http://54.188.87.91:5050/
 * marathon: http://54.188.87.91:8080/
* etcd already running
* run subscriber on ec2 instance
 * `ssh -i helloworld.pem ec2-user@ec2-54-184-184-23.us-west-2.compute.amazonaws.com`
 * `docker run -t -p 5000:5000 -e CONTAINER_HOST_ADDRESS=54.184.184.23 -e CONTAINER_HOST_PORT=5000 -v /home/ec2-user/docker-data:/opt/data 54.189.193.228:5000/subscriber`
 * see container info: http://54.184.184.23:5000/info
* what changes made to images?
 * import a different guestutils file, install python-etcd, explicitly expose ports in Dockerfile
* launch processor (show config.yaml)
 * cassandra, zookeeper
 * kafka
 * processor
 * send curl request to processor 
 * `curl -d raw={"hi"} {{ processor_host }}:{{ processor_port }}/ -i`
* remove services except cassandra
* run cassandra-tester populate to create 100 records in keyspace
* run cassandra-tester test to read from keyspace
* run updater.py cassandra 3 
 * scale up cassandra to 3 nodes
* modify cassandra-tester to only read from last node ip
 * run cassandra-tester test to show it can read from last node only
* send cleanup signal to previous two nodes
 * observe key repartition
 * ssh in and see:
 * `ssh -p 22000 container@{{ host_ip }}`
* comparisons between orchestration tools on github


### Sprint 2 demo

__last sprint:__ deploying containers directly through marathon. loose organization of containers (only know about 
apps and tasks in marathon). marathon apps and tasks are not the best descriptors for dockerized applications and services, however.
did not implement etcd watching - scheduling framework would have had to been application specific to sent messages to specific apps to run nodetool cleanup, for example. 
weaker separation of concerns

__this sprint:__ framework on top of marathon to manage marathon apps and tasks. allows flexibility for managing docker containers
specifically. implemented basic scheduling routines in framework. research on separation of concerns (drawing most ideas from kubernetes).
what should framework, master, slave, applications be responsible for.

__demo goals:__
show basic scheduling tasks
show organization benefits of framework
show monitoring, logging features/responsibilities of mesos-docker tool

1. __architecture__
  * diagram - separation of concerns - what is responsible for what
3. already running: cassandra, presenter, watcher, haproxy, ingestor (all dev)
3. testing haproxy, testing ingestor
4. send traffic
5. rolling update
6. watcher/haproxy -> show etcd key watching
7. logs and metrics in one place
8. fabric (getting started)
