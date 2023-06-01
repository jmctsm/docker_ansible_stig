#!python3

# Still need to expand for creating other parts of config

"""
  Reads in the variables from the configuration vars files and
  then creates a configuration file for that.  This is strictly IOS
  XE.  Requires two arguments.  One for Hostname and one for domain
  name.

  Eventually would like to to either take a EXCEL, JSON, YAML, or other
  file and create the configuration for all including the interfaces.  Currently
  this only applies STIG settings.

  Need to expand for best practices.
"""

import time
import yaml
import os
import argparse


current_time = time.strftime("%Y%m%d_%H%M%S")
# script_run_path = f"{ os.path.expanduser('~') }/docker_ansible_stig/"
script_run_path = f"{ os.getcwd() }/"

transfer_dir = f"{ script_run_path }/transfer/"

config_file_output = f"{ transfer_dir }/iosxe_STIG_config_{ current_time }.txt"
yaml_stig_fixes_file = f"{ script_run_path }stig_yaml_files/iosxe_stig_fixes.yaml"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", help="hostname of the device")
    parser.add_argument("domain_name", help="domain name of the device")
    args = parser.parse_args()
    host_name = args.hostname
    domain_name = args.domain_name

    with open(yaml_stig_fixes_file) as yaml_file:
        fix_dict = yaml.safe_load(yaml_file)
    with open(config_file_output, "w") as config_file:
        config_file.write(f"hostname { host_name }\n")
        config_file.write(f"ip domain-name { domain_name }\n")
        # adding this in with extra spaces so that it creates the
        # crypto key for SSH capability
        config_file.write("crypto key gen rsa mod 2048\n\n\n\n")
        for key in fix_dict.keys():
            config_file.write(f"!{ key }")
            config_file.write("\n")
            config_file.write(f"{ fix_dict[key] }")
            config_file.write("\n\n")


if __name__ == "__main__":
    main()
