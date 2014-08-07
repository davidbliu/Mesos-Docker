FROM davidbliu/etcd_base


RUN pip install fabric

#
# install fabric ec2
#
WORKDIR /opt/cluster
RUN git clone https://github.com/mikery/fabric-ec2.git
WORKDIR /opt/cluster/fabric-ec2
RUN python setup.py install
RUN pip install boto

ADD fabfile.py /opt/cluster/
WORKDIR /opt/cluster



