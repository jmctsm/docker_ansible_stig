#!/python3

from os import system
import subprocess

initial_menu_options = {
    1: "Run Network IOS XE STIG using Ansible (not implemented yet)",
    2: "Generate STIG Config",
    3: "Run Parsers",
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


def option1():
    print("Handle option 'Option 1'")


def generate_configs():
    system("clear")
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
    system("clear")
    while True:
        print_menu(parsers_menu_options)
        option = get_option(parsers_menu_options)
        if option == 1:
            print("Running Network IOS XE STIG XCCDF Parser")
            subprocess.run(["python", "parsers/iosxe_stig_xccdf_parser.py"])
            print("Parser run.  Files in transfer folder. Returning to main menu.")
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
            print("Handle option 'Option 1'")
            option1()
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
