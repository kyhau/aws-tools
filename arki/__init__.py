import click
import logging
import pkg_resources


PACKAGE_NAME = "Arki"


def print_all_console_scripts(package_name):
    """
    Print all console scripts of a package.
    :param package_name: the name of a package installed.
    """
    print(f"Console scripts in {PACKAGE_NAME}:")
    print("------------------------")
    entrypoints = (
        ep for ep in pkg_resources.iter_entry_points("console_scripts")
        if ep.module_name.startswith(package_name.lower())
    )
    for i in entrypoints:
        print(str(i).split("=")[0])
    return entrypoints


def init_logging(log_level=logging.INFO, show_time=False):
    """
    Initialise basic logging to console.
    :param log_level: logging level. Default: INFO
    """
    log_time = "%(asctime)s " if show_time else ""

    logging.basicConfig(
        level=log_level,
        format=f"{log_time}%(levelname)-8s {PACKAGE_NAME}: %(message)s",
    )
    logging.getLogger("botocore").setLevel(logging.CRITICAL)
    logging.getLogger("boto3").setLevel(logging.CRITICAL)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)


@click.command()
def main(package_name=PACKAGE_NAME):
    """
    `arki` prints all console scripts of the arki package.
    """
    print_all_console_scripts(package_name)
