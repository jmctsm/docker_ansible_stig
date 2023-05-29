This is to see if I can build a docker image for ansible in stages.  

Right now the plan to fix file share issues with Ansible is to copy all playbooks to the /home/devops/playbooks directory.  Then a user can run them from there.  

All outputs can be copied to /ansible and it will be copied back to the host machine.

1) Get the image working 
     - docker build -t ansible . 
     - docker run -it -v ${pwd}/transfer:/ansible ansible
    
2) Mount a local file system to pull in an inventory
3) run ansible on inventory and save logs
4) finally would like to have python run on saved files for reporting in PDF, DOC, or XLS


export XML_PATH=/home/$USER/docker_ansible_stig/transfer/
export STIG_PATH=/home/$USER/docker_ansible_stig/playbooks/roles/iosxeSTIG/files/