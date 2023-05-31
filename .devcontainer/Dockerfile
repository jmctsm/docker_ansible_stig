FROM python:3.11.3-bullseye

RUN groupadd --gid 1000 devops \
    && useradd --uid 1000 --gid 1000 -m -s /bin/bash devops \
    && apt-get update \
    && apt-get install -y sudo iputils-ping vim \
    && echo devops ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/devops \
    && chmod 0440 /etc/sudoers.d/devops 

USER devops
WORKDIR /home/devops/
ENV VIRTUALENV=/home/devops/venv
ENV ANSIBLE_CONFIG=/workspaces/docker_ansible_stig/playbooks/ansible.cfg
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"
COPY --chown=devops:devops --chmod=660 requirements_building.txt /home/devops/requirements.txt
RUN python -m pip install --upgrade pip && python -m pip install -r /home/devops/requirements.txt
RUN echo secret > /home/devops/.vault.txt

