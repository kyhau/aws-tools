"""
Define fixtures and prepare settings and environments
"""
from datetime import datetime
import getpass
import logging
from os.path import exists, join
from os import makedirs
import pytest
from shutil import rmtree
import socket
import tempfile


logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)


@pytest.fixture(scope="session")
def unittest_id():
    """Return arki-(username)-(hostname) as the id of the unit tests
    """
    return f"arki-{getpass.getuser()}-{socket.gethostname()}"


@pytest.fixture(scope="session")
def unittest_workspace(unittest_id):
    """
    Create a temporary workspace that will be deleted at the end of the unit testing
    :param unittest_id: id of the unit test
    :return: workspace path and name
    """
    dir_name = join(tempfile.gettempdir(), f"{unittest_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    makedirs(dir_name)

    yield dir_name

    try:
        if exists(dir_name):
            rmtree(dir_name)
    except Exception as e:
        print("Failed to delete {}".format(dir_name))


@pytest.fixture
def sample_configs_1(unittest_workspace):
    default_configs = {
        "aws.lambda.runtime": {"required": True},
        "aws.lambda.timeout": {"required": True},
        "aws.lambda.kmskey.arn": {"required": False},
        "aws.lambda.environment": {"multilines": True},
    }

    lines = [
        "[default]",
        "aws.lambda.runtime = python3.6",
        "aws.lambda.timeout = 60",
        "aws.lambda.kmskey.arn =",
        "aws.lambda.environment =",
        "  x1: v1",
        "  x2: v2",
        "[dev]",
        "aws.lambda.timeout = 90",
    ]
    ini_file = create_sample_ini_file(unittest_workspace, "test1.ini", lines)
    return ini_file, default_configs


def create_sample_ini_file(unittest_workspace, filename, lines):
    """Create sample ini file
    """
    ini_file = join(unittest_workspace, filename)
    with open(ini_file, "w") as f:
        for line in lines:
            f.write(f"{line}\n")
    return ini_file
