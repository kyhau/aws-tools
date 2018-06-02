import click
import configparser
from os.path import expanduser, exists, join
from os import makedirs
import pkg_resources


ARKI_LOCAL_STORE_ROOT = join(expanduser("~"), ".arki")
ARKI_INI_FILE = join(ARKI_LOCAL_STORE_ROOT, "arki.ini")

makedirs(ARKI_LOCAL_STORE_ROOT, 0o755, exist_ok=True)


def print_all_console_scripts(package_name):
    """
    Print all console scripts of a package.
    :param package_name: the name of a package installed.
    """
    print("Console scripts in arki:")
    print("------------------------")
    entrypoints = (
        ep for ep in pkg_resources.iter_entry_points("console_scripts")
        if ep.module_name.startswith(package_name)
    )
    for i in entrypoints:
        print(str(i).split("=")[0])
    return entrypoints


def read_ini(ini_file=ARKI_INI_FILE):
    if exists(ARKI_INI_FILE):
        config = configparser.ConfigParser()
        config.read(ini_file)
        return config
    return {}


def write_ini(config, ini_file=ARKI_INI_FILE):
    with open(ini_file, "w") as configfile:
        config.write(configfile)


@click.command()
def main(package_name="arki"):
    """
    `arki` prints all console scripts of the arki package.
    """
    print_all_console_scripts(package_name)
