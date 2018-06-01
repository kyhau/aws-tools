"""
This utility script adds/updates user_home/.arki/env_store.ini
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


@click.command()
@click.option("--add", "-a", required=False, help="Add new environment variable. TEXT: name=value")
@click.option("--export", "-e", required=False, help="Export environment variable. TEXT: name")
def main(add, export):
    """Manage environment variable store.
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
            if export in env_variables.keys():
                print_export_env(env_dict={export: env_variables[export]})
            else:
                print(f"Environment variable {export} not found in {ENV_STORE_FILE}")
                sys.exit(1)

        else:
            for k, v in env_variables.items():
                print(f"{i}: {k}")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    sys.exit(0)
