

# To build:
# cd sawtooth-ci/ami
# docker build -t build_ami .

# To run:
# cd sawtooth-ci/ami
# docker run -it --rm -v ~/.aws/:/root/.aws/ -v $(pwd)/:/project -v ~/.ssh/:/root/.ssh build_ami 

FROM ubuntu

RUN apt-get update && \
    apt-get install -qy \
    python \
    python-pip && \
    pip install \
    ansible \
    awscli --upgrade --user && \
    export PATH=~/.local/bin:$PATH && \
    mkdir /etc/ansible

ENV ANSIBLE_HOST_KEY_CHECKING=False
ENV PATH=~/.local/bin:$PATH

WORKDIR /project

ENTRYPOINT bin/make_ami
