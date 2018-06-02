"""
This utility script adds/updates <user_home>/.arki/env_store.ini
"""
import click
from collections import OrderedDict
from os.path import expanduser, exists, join
from os import makedirs
import sys
from arki.system import print_export_env


ENV_STORE_ROOT = join(expanduser("~"), ".arki")
ENV_STORE_FILE = join(ENV_STORE_ROOT, "env_store.ini")


def write_file(env_variables, filename=ENV_STORE_FILE):
    """Write (rewrite) env variables to file
    """
    with open(filename, "w") as c_file:
        for k, v in env_variables.items():
            c_file.write(f"{k}={v}\n")


def check_env_valid(env_variables, input):
    """Check if the given env name exists.
    """
    if input.isdigit():
        target_index = int(input)
        if target_index >= len(env_variables):
            print(f"Profile index {input} not found")
            return None

        index = 0
        for k, v in env_variables.items():
            if index == target_index:
                break
            index+=1
        return k
    elif input in env_variables.keys():
        return input
    else:
        print(f"Environment variable {input} not found in {ENV_STORE_FILE}")
        return None

@click.command()
@click.option("--add", "-a", required=False, help="Add new environment variable. TEXT: name=value")
@click.option("--export", "-e", required=False, help="Print the command to export a environment variable. Valid values: The name or its index returned from running `env_store`.")
def main(add, export):
    """
    env_store returns the list of environment variables stored in ~/.arki/env_store.ini.
    Use -a to add new variable. Use -e to print the command to export it as environment variable,
    by specifying the variable name (e.g. env_store -e TEST_MODE) or the index of the variables
    printed from running `env_store` (e.g. env_store -e 1).
    All environment variables are stored in plain text. Do not use this script to store secrets or
    credentials.
    """
    try:
        makedirs(ENV_STORE_ROOT, 0o755, exist_ok=True)

        env_variables = OrderedDict()
        if exists(ENV_STORE_FILE):
            with open(ENV_STORE_FILE, "r") as c_file:
                for line in c_file.readlines():
                    if not line.startswith("#"):
                        k, v = line.split("=")
                        env_variables[k.strip()] = v.strip()

        if add:
            k, v = add.split("=")
            k, v = k.strip(), v.strip()

            if k in env_variables.keys():
                if v == env_variables[k]:
                    print(f"{k} already exists")
                else:
                    env_variables[k] = v
                    write_file(env_variables)
                    print(f"{k} updated")
            else:
                env_variables[k] = v
                write_file(env_variables)
                print(f"{k} added")

        elif export:
            env_name = check_env_valid(env_variables, export)
            if env_name:
                print_export_env(env_dict={env_name: env_variables[env_name]})
            else:
                sys.exit(1)

        else:
            index = 0
            for k, v in env_variables.items():
                print(f"{index}: {k} = {v}")
                index+=1

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    sys.exit(0)
