import logging
from os.path import abspath, dirname, exists
import os
import pkg_resources

PACKAGE_NAME = "arki_common"


def init_logging(
        name=PACKAGE_NAME,
        log_level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        log_file=None
):
    """
    Initialise basic logging to console (and file).

    E.g. format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    """
    #logging.basicConfig(
    #    level=log_level,
    #    format=f"{log_time}%(levelname)-8s {package_name}: %(message)s",
    #)
    logging.getLogger().setLevel(log_level)
    logging.getLogger("botocore").setLevel(logging.CRITICAL)
    logging.getLogger("boto3").setLevel(logging.CRITICAL)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    formatter = logging.Formatter(format)

    ch = logging.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if log_file is not None:
        create_directory_if_not_exist(log_file)
        fh = logging.FileHandler(log_file)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def create_directory_if_not_exist(file_path):
    """
    Create directory for the given file path if it does not exist

    :param file_path: A file name with path
    :raise IOError: if failed to create directory
    """
    try:
        base_dir = dirname(abspath(file_path))
        if not exists(base_dir):
            os.makedirs(base_dir)
    except Exception as e:
        raise IOError(f"Failed to create {base_dir}: {e}")


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
