#!/python3

"""
This script will create a menu that a user can then select what they want
to do.  It is setup so that as more features are added the menus can
be expanded.

If things get to large this could all possbily be so that a selection calls
a different file.  Have to wait and see how this all goes.
"""

import os
import subprocess

initial_menu_options = {
    1: "Run Network IOS XE STIG using Ansible",
    2: "Generate STIG Config",
    3: "Run Parsers",
    4: "Exit",
}

run_ansible_options = {
    1: "Run Ansible IOS XE STIG in check mode",
    2: "Run Ansible IOS XE STIG in appy mode (not implemented yet)",
    3: "Return to Main Menu",
    4: "Exit",
}


parsers_menu_options = {
    1: "Network IOS XE STIG XCCDF",
    2: "Return to Main Menu",
    3: "Exit",
}

config_menu_options = {}


def print_menu(menu_options):
    """
    Using the menu option dictionary provided,
    this will then create a menu for the user
    to select from
    """
    for key in menu_options.keys():
        print(key, "--", menu_options[key])


def set_ansible_environment_variables(
    config_fle_location,
    stig_ansible_iosxe=False,
):
    """
    to use the correct call this uses environment variables
    to set the correct Ansible configuration file
    if the IOSXE variable is set then certain environment
    variables need to be set for the callback
    """
    os.environ["ANSIBLE_CONFIG"] = config_fle_location
    if stig_ansible_iosxe:
        os.environ["XML_PATH"] = "./transfer/"
        os.environ["STIG_PATH"] = "./playbooks/roles/iosxeSTIG/files/"
    return


def unset_ansible_environment_variables(
    stig_ansible_iosxe=False,
):
    """
    Once Ansible runs, this will clean up all
    environment variables set.  If running this
    against an IOS XE box, need to clean up the
    PATH variables as well
    """
    del os.environ["ANSIBLE_CONFIG"]
    if stig_ansible_iosxe:
        del os.environ["XML_PATH"]
        del os.environ["STIG_PATH"]
    return


def call_subprocess(arg_list):
    """
    Will take the arguments for subprocess and pass them into a
    try/except filter in case something messes up
    """
    try:
        subprocess.run(arg_list, check=True)
    except subprocess.CalledProcessError:
        return
    return


def run_ansible():
    """
    Run ansible based on options being selected
    for different devices
    """
    os.system("clear")
    while True:
        # print the menu for run ansible then get
        # user selection.  Also let the user know that the
        # options 1 and 2 run the XCCDF parser (may take this out
        # if more run it).
        print_menu(run_ansible_options)
        print("Options 1 and 2 will also run the XCCDF parser")
        option = get_option(parsers_menu_options)
        # if option 1 or 2, set configuration file for IOS XE STIG
        # and set that this is the IOSXE STIG
        if option == 1 or option == 2:
            print("Running Ansible Network IOS XE STIG STIG in check mode")
            set_ansible_environment_variables(
                config_fle_location="./playbooks/iosxe_stig_ansible.cfg",
                stig_ansible_iosxe=True,
            )
            # option 1 runs this in check mode
            if option == 1:
                call_subprocess(
                    [
                        "ansible-playbook",
                        "playbooks/iosxe_stig.yml",
                        "--check",
                    ],
                )
            # option 2 runs this in apply mode
            elif option == 2:
                call_subprocess(
                    [
                        "ansible-playbook",
                        "playbooks/iosxe_stig.yml",
                    ],
                )
            # once ansible runs, parser will run to make word doc, JSON file,
            # and configuration file.  Afterwards all environment variables
            # created are unset and returns to the main menu
            print("Ansible complete.  Running parser now.")
            call_subprocess(["python", "parsers/iosxe_stig_xccdf_parser.py"])
            print("Parser complete.  Files in transfer folder. ",
                  "Returning to main menu.")
            unset_ansible_environment_variables(stig_ansible_iosxe=True)
            return
        # returns to the main menu
        if option == 3:
            return
        # Exits the entire program
        if option == 4:
            print("Exiting the program")
            exit()


def generate_configs():
    """
    Generate configs for devices based on different requirements
    """
    os.system("clear")
    while True:
        xml_files = os.listdir(f"{ os.getcwd()}/xml_files/")
        counter = 1
        for file in xml_files:
            config_menu_options[counter] = file
            counter += 1
        return_number = counter
        exit_number = counter + 1
        config_menu_options[return_number] = "Return to Main Menu"
        config_menu_options[exit_number] = "Exit"
        # print menu options and get user input
        print_menu(config_menu_options)
        option = get_option(parsers_menu_options)
        # returns to the main menu
        if option == return_number:
            return
        # Exits the entire program
        elif option == exit_number:
            print("Exiting the program")
            exit()
        # Creates the IOS XE config.  Requires the hostname
        # and device domain name.  Once gotten then pass to the
        # config generator and once done return to the main menu
        elif "IOS-XE" in config_menu_options[option]:
            print("Will create STIG IOS XE config")
            hostname = get_string_input("device hostname")
            domain_name = get_string_input("device domain name")
            full_file_path = f"{ os.getcwd()}/xml_files/{ config_menu_options[option] }"
            call_subprocess(
                [
                    "python",
                    "disa_scap_converters/iosxe_scap_converter.py",
                    f"{ hostname }",
                    f"{ domain_name }",
                    f"{ full_file_path }"
                ],
            )
            print(
                "Config generator run.  Files in transfer folder. ",
                "Returning to main menu.",
            )
            return


def get_string_input(what_you_want):
    """
    keeps trying to get the information from the user and
    repeats until correct.
    """
    while True:
        try:
            string_input = str(input(f"Enter { what_you_want }: "))
            return string_input
        except ValueError:
            print("Wrong input. Please try again")


def run_parsers():
    """
    Print menu and get user info.  Option 1 run this against the IOS
    XE XCCDF output from from Ansible.  Once complete, returns to main
    menu
    """
    os.system("clear")
    while True:
        print_menu(parsers_menu_options)
        option = get_option(parsers_menu_options)
        if option == 1:
            print("Running Network IOS XE STIG XCCDF Parser")
            call_subprocess(["python", "parsers/iosxe_stig_xccdf_parser.py"])
            print("Parser run.  Files in transfer folder.  ",
                  "Returning to main menu.")
            return
        # returns to the main menu
        if option == 2:
            return
        # Exits the entire program
        if option == 3:
            print("Exiting the program")
            exit()


def get_option(menu_options):
    """
    this continues to run until the user enters a number
    then returns the number.
    """
    while True:
        try:
            option = int(input("Enter your choice: "))
            return option
        except ValueError:
            print(
                "Wrong input. Please enter a number between 1 and ",
                len(menu_options),
                ".",
            )
            print_menu(menu_options)


def main():
    """
    creates the main menu for user selection.
    This can expand as more options are added.
    If user does not enter a correct value,
    repeat the whole thing
    """
    while True:
        print_menu(initial_menu_options)
        option = get_option(initial_menu_options)
        if option == 1:
            run_ansible()
        elif option == 2:
            generate_configs()
        elif option == 3:
            run_parsers()
        # Exits the entire program
        elif option == 4:
            print("Thank you for using this program.")
            exit()
        else:
            print(
                "Invalid option. Please enter a number between 1 and ",
                len(initial_menu_options),
                ".",
            )


if __name__ == "__main__":
    main()
