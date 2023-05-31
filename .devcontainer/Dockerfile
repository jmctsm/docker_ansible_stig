FROM python:3.11.3-bullseye

RUN groupadd --gid 1000 devops \
    && useradd --uid 1000 --gid 1000 -m -s /bin/bash devops \
    && apt-get update \
    && apt-get install -y sudo iputils-ping vim \
    && echo devops ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/devops \
    && chmod 0440 /etc/sudoers.d/devops 

USER devops
RUN mkdir /home/devops/docker_ansible_stig/
WORKDIR /home/devops/docker_ansible_stig/
ENV VIRTUALENV=/home/devops/docker_ansible_stig/venv
ENV ANSIBLE_CONFIG=/workspaces/docker_ansible_stig/playbooks/ansible.cfg
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"
RUN python -m pip install --upgrade pip 
RUN echo secret > /workspaces/docker_ansible_stig/.vault.txt

