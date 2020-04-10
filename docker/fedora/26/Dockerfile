FROM fedora:26
RUN dnf update -y && \
    dnf install -y python3-pip wget libffi-devel python3-devel gcc git which && \
    pip3 install --upgrade pip
RUN alternatives --install /usr/bin/python python $(which python3)
RUN alternatives --install /usr/bin/pip pip $(which pip3)
