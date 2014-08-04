FROM davidbliu/etcd_base

#
# install sshd
#
RUN apt-get install -y sudo ntp openssh-server supervisor
RUN mkdir -p /var/run/sshd
RUN adduser --gecos "" container
RUN echo 'container:container' | sudo -S chpasswd
RUN echo 'container ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
RUN sed -i -e 's/^\(session\s\+required\s\+pam_loginuid.so$\)/#\1/' /etc/pam.d/sshd

ADD . /opt/tester
WORKDIR /opt/tester
# Expose ports.
EXPOSE 22

CMD python -u boot.py