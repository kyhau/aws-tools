import logging
import os
import sys


def is_linux():
    """
    Check if the current platform is Linux.
    :return: True if the current platform is Linux; False otherwise
    """
    return sys.platform.startswith("linux")


def is_windows():
    """
    Check if the current platform is Windows.
    :return: True if the current platform is Windows; False otherwise
    """
    return sys.platform.startswith("win")


def print_export_env(env_dict):
    """
    Print the command(s) for exporting environment variables to current platform
    :param env_dict: Dictionary containing the environment variables
    """
    if is_linux():
        cmd_env_str = "export {}={}"
    elif is_windows():
        cmd_env_str = 'set "{}={}"'
    else:
        raise Exception("Platform not supported")

    print("Copy and invoke the following command(s):")
    print("-----------------------------------------")
    for k, v in env_dict.items():
        print(cmd_env_str.format(k, v))
    print("-----------------------------------------")


def run_command(command):
    """
    Run a command
    :param command: command string
    :return: return code (0 means all good)
    """
    logging.info(command)
    ret_code = os.system(command)

    logging.info(f"Command return code: {ret_code}")
    return ret_code
