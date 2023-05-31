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

Things to work on
call main script
    present options
        run network IOS XE stig in check mode
            ask to run in check mode or apply mode
            run ansible playbook with specific ansible.cfg that uses stig call back script
            run xccdf network parser script to make docs and config for unapplied stigs
            set environment variables for stig and export
        run network IOS XE STIG in apply mode
            run ansible playbook with specific ansible.cfg that uses stig call back script
            run xccdf network parser script to make docs and config for unapplied stigs
            set environment variables for stig and export
        generate IOS XE STIG config 
            use a menu system to put in hostname and other options
                IOS xe still needs the ability to read a file and make a config
                add in username and password as well
        run parsers
            IOS XE currently
        parser of STIG SCAP file to config generator
        grow this as more options are added
        




would like to have
    dockerfile that runs all this in a virtual environment
        have the file but not exactly working yet.  Working on python first then that.
    webpage with buttons to control all this
    ability to generate an inventory file from webpage input
