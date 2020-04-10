FROM ubuntu:16.04
RUN apt-get update && \
    apt-get install -y python3-pip wget libffi-dev git && \
    pip3 install --upgrade pip
RUN update-alternatives --install /usr/bin/python python $(which python3) 10
RUN update-alternatives --install /usr/bin/pip pip $(which pip3) 10 
