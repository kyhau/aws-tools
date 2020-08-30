import logging
import os
from os.path import basename, dirname

import pkg_resources

PACKAGE_NAME = basename(dirname(__file__))


def print_all_console_scripts(package_name=PACKAGE_NAME):
    """
    Print all console scripts of a package.
    :param package_name: the name of a package installed.
    """
    print(f"Console scripts in {package_name}:")
    print("------------------------")
    entrypoints = (
        ep for ep in pkg_resources.iter_entry_points("console_scripts")
        if ep.module_name.startswith(package_name.lower())
    )
    for i in entrypoints:
        print(str(i).split("=")[0])
    return entrypoints


if __name__ == "__main__":
    print_all_console_scripts()
