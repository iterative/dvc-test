FROM ubuntu:18.04
RUN apt-get update && \
    apt-get install -y python3-pip wget libffi-dev git && \
    pip3 install --upgrade pip
RUN update-alternatives --install /usr/bin/python python $(which python3)
RUN update-alternatives --install /usr/bin/pip pip $(which pip3)
