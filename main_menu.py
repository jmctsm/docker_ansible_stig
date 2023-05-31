#!/python3

import os
import subprocess

initial_menu_options = {
    1: "Run Network IOS XE STIG using Ansible (not implemented yet)",
    2: "Generate STIG Config",
    3: "Run Parsers",
    4: "Exit",
}

run_ansible_options = {
    1: "Run Ansible IOS XE STIG in check mode",
    2: "Run Ansible IOS XE STIG in appy mode",
    3: "Return to Main Menu",
    4: "Exit",
}


parsers_menu_options = {
    1: "Network IOS XE STIG XCCDF",
    2: "Return to Main Menu",
    3: "Exit",
}

config_menu_options = {
    1: "Network IOS XE STIG Config",
    2: "Return to Main Menu",
    3: "Exit",
}


def print_menu(menu_options):
    for key in menu_options.keys():
        print(key, "--", menu_options[key])


def set_ansible_environment_variables(
    config_fle_location,
    stig_ansible_iosxe=False,
):
    # subprocess.run([f"ANSIBLE_CONFIG={ config_fle_location }"])
    os.environ["ANSIBLE_CONFIG"] = config_fle_location
    if stig_ansible_iosxe:
        # subprocess.run(["XML_PATH=./transfer/"])
        # subprocess.run(["STIG_PATH=./playbooks/roles/iosxeSTIG/files/"])
        os.environ["XML_PATH"] = "./transfer/"
        os.environ["STIG_PATH"] = "./playbooks/roles/iosxeSTIG/files/"
    return


def unset_ansible_environment_variables(
    stig_ansible_iosxe=False,
):
    # subprocess.run(["unset", "ANSIBLE_CONFIG"])
    del os.environ["ANSIBLE_CONFIG"]
    if stig_ansible_iosxe:
        # subprocess.run(["unset", "XML_PATH"])
        # subprocess.run(["unset", "STIG_PATH"])
        del os.environ["XML_PATH"]
        del os.environ["STIG_PATH"]
    return


def run_ansible():
    os.system("clear")
    while True:
        print_menu(run_ansible_options)
        option = get_option(parsers_menu_options)
        print("Options 1 and 2 will also run the XCCDF parser")
        if option == 1 or option == 2:
            print("Running Ansible Network IOS XE STIG STIG in check mode")
            set_ansible_environment_variables(
                config_fle_location="./playbooks/iosxe_stig_ansible.cfg",
                stig_ansible_iosxe=True,
            )
            if option == 1:
                subprocess.run(
                    [
                        "ansible-playbook",
                        "playbooks/iosxe_stig.yml",
                        "--check",
                    ]
                )
            elif option == 2:
                subprocess.run(
                    [
                        "ansible-playbook",
                        "playbooks/iosxe_stig.yml",
                    ]
                )
            print("Ansible complete.  Running parser now.")
            subprocess.run(["python", "parsers/iosxe_stig_xccdf_parser.py"])
            print("Parser complete.  Files in transfer folder. Returning to main menu.")
            unset_ansible_environment_variables(stig_ansible_iosxe=True)
            return
        if option == 3:
            return
        if option == 4:
            print("Exiting the program")
            exit()


def generate_configs():
    os.system("clear")
    while True:
        print_menu(config_menu_options)
        option = get_option(parsers_menu_options)
        if option == 1:
            print("Will create network IOS XE config")
            hostname = get_string_input("device hostname")
            domain_name = get_string_input("device domain name")
            subprocess.run(
                [
                    "python",
                    "config_generators/iosxe_stig_config_generator.py",
                    f"{ hostname }",
                    f"{ domain_name }",
                ]
            )
            print(
                "Config generator run.  Files in transfer folder. ",
                "Returning to main menu.",
            )
            return
        if option == 2:
            return
        if option == 3:
            print("Exiting the program")
            exit()


def get_string_input(what_you_want):
    while True:
        try:
            string_input = str(input(f"Enter { what_you_want }: "))
            return string_input
        except ValueError:
            print("Wrong input. Please try again")


def run_parsers():
    os.system("clear")
    while True:
        print_menu(parsers_menu_options)
        option = get_option(parsers_menu_options)
        if option == 1:
            print("Running Network IOS XE STIG XCCDF Parser")
            subprocess.run(["python", "parsers/iosxe_stig_xccdf_parser.py"])
            print("Parser run.  Files in transfer folder. Returning to main menu.")
            return
        if option == 2:
            return
        if option == 3:
            print("Exiting the program")
            exit()


def get_option(menu_options):
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
    while True:
        print_menu(initial_menu_options)
        option = get_option(initial_menu_options)
        if option == 1:
            run_ansible()
        elif option == 2:
            generate_configs()
        elif option == 3:
            run_parsers()
        elif option == 4:
            print("Thanks message before exiting")
            exit()
        else:
            print(
                "Invalid option. Please enter a number between 1 and ",
                len(initial_menu_options),
                ".",
            )


if __name__ == "__main__":
    main()
