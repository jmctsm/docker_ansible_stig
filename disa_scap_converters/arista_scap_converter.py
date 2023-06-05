#!python

"""
Reads in the XCCDF file from the DISA STIG to then make a config template
"""

import os
import argparse
import common_funcs

current_dir = f"{ os.getcwd() }"

output_path = f"{ current_dir }/transfer/"


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
            rule_sev = common_funcs.fix_severity_wording(xml_file_list[counter][-7:-1])
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
                "rule_severity": rule_sev,
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
    line_counter = 0
    split_text = fix_text_str.split("\n")
    config_new_words = ["configure\n", "configure\r", "configure", "config\n",
                        "config\r", "configure", "config",]
    startwith_tuple = ("logging level", "aaa authentication",
                       "dot1x system-auth-control", "username ")
    while line_counter < len(split_text):
        if "(con" in split_text[line_counter]:
            counter = 0
            while counter < len(split_text[line_counter]):
                if split_text[line_counter][counter] == '#':
                    counter += 1
                    return_string += f"{ split_text[line_counter][counter:] }\n"
                    counter = len(split_text[line_counter]) + 10
                counter += 1
        elif (split_text[line_counter] in config_new_words
              or split_text[line_counter].startswith(startwith_tuple)):
            return_string += f"{ split_text[line_counter] }\n"
            line_counter += 1
            while line_counter < len(split_text) and not split_text[line_counter] == "":
                return_string += f"{ split_text[line_counter] }\n"
                line_counter += 1
        line_counter += 1
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
                fix_list = rule_info['rule_fix_ref'].split("\n")
                for line in fix_list:
                    config_file.write(f"! { line }\n")
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
    xml_file_list = common_funcs.get_file_contents(scap_file)
    xml_file_dict = create_dict(xml_file_list)
    generate_config(xml_file_dict, scap_file, host_name, domain_name)


if __name__ == "__main__":
    main()
