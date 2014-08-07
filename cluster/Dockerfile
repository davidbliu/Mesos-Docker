FROM davidbliu/etcd_base


RUN pip install fabric

#
# install fabric ec2
#
WORKDIR /opt/cluster
RUN git clone https://github.com/mikery/fabric-ec2.git
WORKDIR /opt/cluster/fabric-ec2
RUN python setup.py install

#
# install sshd
#
RUN apt-get install -y sudo ntp openssh-server supervisor
RUN mkdir -p /var/run/sshd
RUN adduser --gecos "" container
RUN echo 'container:container' | sudo -S chpasswd
RUN echo 'container ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN sed -i -e 's/^\(session\s\+required\s\+pam_loginuid.so$\)/#\1/' /etc/pam.d/sshd

ADD fabfile.py /opt/cluster
ADD boot.py /opt/cluster
WORKDIR /opt/cluster

CMD python -u boot.py


