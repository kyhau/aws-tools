import sys


def is_linux():
    return sys.platform.startswith("linux")


def is_windows():
    return sys.platform.startswith("win")


def print_export_env(env_dict):
    """Export environment variables of the given dictionary
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

