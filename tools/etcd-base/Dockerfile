# enable python etcd interaction
FROM ubuntu:14.04
MAINTAINER David Liu <davidbliu@gmail.com>
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update
RUN apt-get -y upgrade

#
# install python
#
RUN apt-get -y install python python-pip git

#
# add python-etcd 
#
WORKDIR /opt/pyetcd
RUN apt-get -y install git
RUN git clone https://github.com/jplana/python-etcd.git
WORKDIR /opt/pyetcd/python-etcd
#
# install python-etcd dependencies
#
RUN apt-get update
RUN apt-get -y install python-dev
RUN apt-get -y install libffi-dev
RUN apt-get -y install libssl-dev 
RUN python setup.py install

WORKDIR /opt/pyetcd
