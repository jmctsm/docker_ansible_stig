#!python

"""
Reads in the XCCDF file from the DISA STIG to then make a config template
"""

import os
import argparse

current_dir = f"{ os.getcwd() }"

# xml_dir = f"{ current_dir }/xml_files"

# scap_file = f"{ xml_dir }/U_Cisco_IOS-XE_Switch_L2S_STIG_V2R3_Manual-xccdf.xml"

output_path = f"{ current_dir }/transfer/"


def get_file_contents(file_to_parse):
    """
    read in the file contents into a list
    """
    with open(file_to_parse, encoding="utf8") as input_file:
        input_contents = input_file.read()
    return input_contents.split("><")


def fix_severity_wording(severity):
    """
    Some severities get messed up due to length not being the same
    this fixes that so that makes it consistent
    """
    if "high" in severity.lower():
        return "high"
    if "low" in severity.lower():
        return "low"
    if "medium" in severity.lower():
        return "medium"


def create_dict(xml_file_list):
    """
    Takes a list where each line is XML minus the beginning ">"
    Converts that to a dictionary
    """
    counter = 0
    return_dict = {}
    while counter < len(xml_file_list):
        if xml_file_list[counter].startswith("Group"):
            rule_id = xml_file_list[counter][10:-1]
            counter += 1
            rule_title = xml_file_list[counter][6:-7]
            counter += 2
            rule_severity = fix_severity_wording(xml_file_list[counter][-7:-1])
            counter += 2
            rule_long_title = xml_file_list[counter][6:-7]
            counter += 1
            # if the line does not start with fixtext then increment
            while not xml_file_list[counter].startswith("fixtext "):
                counter += 1
            # second counter is to get character counts used for
            # getting the rule fix ref.  This resets to 0 during each iteration
            second_counter = 0
            while not xml_file_list[counter][second_counter] == ">":
                second_counter += 1
            second_counter += 1
            rule_fix_ref = xml_file_list[counter][second_counter:-9]
            # once this runs, then we have the files so we now need
            # to create the dictionary that will hold all of this
            # for use later.  Key is the rule ID and each value is
            # another dictionary of values
            return_dict[rule_id] = {
                "rule_title": rule_title,
                "rule_severity": rule_severity,
                "rule_long_title": rule_long_title,
                "rule_fix_ref": rule_fix_ref,
                "fix_commands": fix_commands(rule_fix_ref)
            }
        counter += 1
    # returns the final result dictionary for creating files
    return return_dict


def fix_commands(fix_text_str):
    """
    Takes a string for the fix text and returns the commands within the text
    that need to be applied to a device
    """
    return_string = ""
    for line in fix_text_str.split("\n"):
        if "(con" in line:
            counter = 0
            while counter < len(line):
                if line[counter] == '#':
                    counter += 1
                    return_string += f"{ line[counter:] }\n"
                    counter = len(line) + 10
                counter += 1
    return return_string


def generate_config(xml_dict, input_file, host_name, domain_name):
    """
    generates a configuration using the SCAP file
    XML dict is a dictionary of the inputs in the file
    SCAP file is the original file name so that it can be
    included in the output file
    """
    # takes the file path to get the file name as the last
    # element of the list and trims the last four characters
    # so no .xml
    file_name = (input_file.split('/'))[-1][:-4]
    output_file = f"{ output_path }{ file_name }_config.txt"
    with open(output_file, "w", encoding="utf8") as config_file:
        disclaimer = """
! there are many variables still left to work but
! this is a good start to work from
        """
        config_file.write(f"{ disclaimer }\n\n")
        config_file.write(f"hostname { host_name }\n")
        config_file.write(f"ip domain-name { domain_name }\n")
        # adding this in with extra spaces so that it creates the
        # crypto key for SSH capability
        config_file.write("crypto key gen rsa mod 2048\n\n\n\n")
        for rule_id, rule_info in xml_dict.items():
            config_file.write(f"! { rule_id }\n")
            config_file.write(f"! severity: { rule_info['rule_severity'] }\n")
            if rule_info["fix_commands"]:
                config_file.write(rule_info["fix_commands"])
            else:
                config_file.write(f"! { rule_info['rule_fix_ref'] }")
            config_file.write("\n\n")


def main():
    """
    main execution of the program
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("hostname", help="hostname of the device",)
    parser.add_argument("domain_name", help="domain name of the device",)
    parser.add_argument("xml_xccdf_file",
                        help="Complete path to XCCDF file to create config from",)
    args = parser.parse_args()
    if os.path.exists(args.xml_xccdf_file):
        scap_file = args.xml_xccdf_file
    else:
        print(f"{ args.xml_xccdf_file } does not exists.  Exiting")
        return
    host_name = args.hostname
    domain_name = args.domain_name
    xml_file_list = get_file_contents(scap_file)
    xml_file_dict = create_dict(xml_file_list)
    generate_config(xml_file_dict, scap_file, host_name, domain_name)


if __name__ == "__main__":
    main()
