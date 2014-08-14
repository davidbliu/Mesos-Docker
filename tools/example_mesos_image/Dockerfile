FROM 54.189.193.228:5000/mesos-base

RUN apt-get -y update

ADD . /opt/example
WORKDIR /opt/example
# Expose ports.
EXPOSE 22

CMD python -u boot.py