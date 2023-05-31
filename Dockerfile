FROM jmctsm/rocky_ansible:2.0

RUN dnf install iputils -y

COPY . /home/devops/
RUN chown -R devops:devops /home/devops/ && chmod -x /home/devops/.vault.txt
WORKDIR /home/devops/playbooks
#ENV ANSIBLE_CONFIG=/ansible/playbooks/ansible.cfg 
#ENV STIG_PATH=/home/devops/roles/iosxeSTIG/files/U_Cisco_IOS-XE_Router_NDM_STIG_V2R1_Manual-xccdf.xml
#ENV XML_PATH=/ansible
USER devops