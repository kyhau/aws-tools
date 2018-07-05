"""
This utility script adds/updates <user_home>/.arki/env_store.ini
"""
import click
from collections import OrderedDict
import logging
from os.path import exists, join
from os import makedirs
import sys
from arki.configs import ARKI_LOCAL_STORE_ROOT
from arki.system import print_export_env
from arki import init_logging


# Default configuration file location
ENV_STORE_FILE = join(ARKI_LOCAL_STORE_ROOT, "env_store.ini")


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
            raise Exception(f"Profile index {input} not found")

        index = 0
        for k, v in env_variables.items():
            if index == target_index:
                break
            index+=1
        return k

    elif input in env_variables.keys():
        return input

    else:
        raise Exception(f"Environment variable {input} not found in {ENV_STORE_FILE}")


@click.command()
@click.option("--add", "-a", required=False, help="Add new environment variable. TEXT: name=value")
@click.option("--export", "-e", required=False, help="Print the command to export a environment variable. Valid values: The name or its index returned from running `env_store`.")
def main(add, export):
    """
    env_store returns the list of environment variables stored in ~/.arki/env_store.ini.

    Use -a to add new variable.

    Use -e to print the command to export it as environment variable, by specifying the variable name
    (e.g. env_store -e TEST_MODE) or the index of the variables printed from running `env_store`
    (e.g. env_store -e 1).

    All environment variables are stored in plain text. Do not use this script to store secrets or
    credentials.
    """

    try:
        init_logging()

        makedirs(ARKI_LOCAL_STORE_ROOT, 0o755, exist_ok=True)

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
                    logging.info(f"{k} already exists")
                else:
                    env_variables[k] = v
                    write_file(env_variables)
                    logging.info(f"{k} updated")
            else:
                env_variables[k] = v
                write_file(env_variables)
                logging.info(f"{k} added")

        elif export:
            env_name = check_env_valid(env_variables, export)
            print_export_env(env_dict={env_name: env_variables[env_name]})

        else:
            index = 0
            for k, v in env_variables.items():
                print(f"{index}: {k} = {v}")
                index+=1

    except Exception as e:
        logging.error(e)
        sys.exit(1)

    sys.exit(0)
