"""
Define fixtures and prepare settings and environments
"""

import getpass
import logging
import socket
import tempfile
from datetime import datetime
from os import makedirs
from os.path import exists, join
from shutil import rmtree

import pytest
from botocore.exceptions import ClientError
from helper.logger import init_logging

init_logging(log_level=logging.DEBUG)


@pytest.fixture(scope="session")
def unittest_id():
    """Return test-(username)-(hostname) as the id of the unit tests"""
    return f"test-{getpass.getuser()}-{socket.gethostname()}"


@pytest.fixture(scope="session")
def unittest_workspace(unittest_id):
    """
    Create a temporary workspace that will be deleted at the end of the unit testing
    :param unittest_id: id of the unit test
    :return: workspace path and name
    """
    dir_name = join(
        tempfile.gettempdir(), f"{unittest_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    )
    makedirs(dir_name, exist_ok=True)

    yield dir_name

    try:
        if exists(dir_name):
            rmtree(dir_name)
            logging.debug(f"Removing workspace {dir_name}")
    except Exception:
        logging.error("Failed to delete {}".format(dir_name))


@pytest.fixture
def mock_boto3_client(mocker):
    """Mock boto3 client for AWS API testing."""
    return mocker.patch("boto3.client", autospec=True)


@pytest.fixture
def mock_boto3_session(mocker):
    """Mock boto3 Session for multi-account testing."""
    return mocker.patch("boto3.session.Session", autospec=True)


@pytest.fixture
def sample_aws_tags():
    """Sample AWS resource tags for testing."""
    return [
        {"Key": "Name", "Value": "TestResource"},
        {"Key": "Environment", "Value": "Production"},
        {"Key": "Owner", "Value": "TeamA"},
        {"Key": "CostCenter", "Value": "Engineering"},
    ]


@pytest.fixture
def sample_json_data():
    """Sample JSON data for file I/O testing."""
    return {
        "string": "test",
        "number": 42,
        "float": 3.14,
        "boolean": True,
        "null": None,
        "array": [1, 2, 3],
        "object": {"nested": "value"},
    }


@pytest.fixture
def sample_csv_data():
    """Sample CSV data for testing."""
    return [
        ["Name", "Age", "City"],
        ["Alice", "30", "New York"],
        ["Bob", "25", "San Francisco"],
        ["Charlie", "35", "Seattle"],
    ]


@pytest.fixture
def sample_configs_1(unittest_workspace):
    """Sample INI configuration file with multiple sections."""
    default_configs = {
        "aws.lambda.runtime": {"required": True},
        "aws.lambda.timeout": {"required": True},
        "aws.lambda.kmskey.arn": {"required": False},
        "aws.lambda.environment": {"multilines": True},
    }

    context = """
[default]
aws.lambda.runtime = python3.6
aws.lambda.timeout = 60
aws.lambda.kmskey.arn =
aws.lambda.environment =
  x1: v1
  x2: v2

[dev]
aws.lambda.timeout = 90
    """

    ini_file = write_file(unittest_workspace, "test1.ini", context)
    return ini_file, default_configs


@pytest.fixture
def sample_cloudformation_template(unittest_workspace):
    """Sample CloudFormation template for testing."""
    template_content = """
AWSTemplateFormatVersion: '2010-09-09'
Description: Test CloudFormation Template

Parameters:
  EnvironmentName:
    Type: String
    Default: dev

Resources:
  TestBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'test-bucket-${EnvironmentName}'

Outputs:
  BucketName:
    Value: !Ref TestBucket
    """
    template_file = write_file(unittest_workspace, "template.yaml", template_content)
    return template_file


@pytest.fixture
def sample_sql_queries(unittest_workspace):
    """Sample SQL query files for testing."""
    queries = {
        "select.sql": "SELECT * FROM users WHERE active = 1;",
        "insert.sql": "INSERT INTO users (name, email) VALUES ('test', 'test@example.com');",
        "update.sql": "UPDATE users SET active = 0 WHERE id = 1;",
    }

    query_files = {}
    for filename, content in queries.items():
        query_files[filename] = write_file(unittest_workspace, filename, content)

    return query_files


@pytest.fixture
def mock_client_error():
    """Factory fixture for creating ClientError instances."""

    def _make_error(error_code, message="Test error"):
        return ClientError({"Error": {"Code": error_code, "Message": message}}, "test_operation")

    return _make_error


def write_file(unittest_workspace, filename, context):
    """Create sample file in workspace.

    Args:
        unittest_workspace: Path to workspace directory
        filename: Name of file to create
        context: Content to write to file

    Returns:
        Full path to created file
    """
    file_path = join(unittest_workspace, filename)
    with open(file_path, "w") as f:
        f.write(context)
    return file_path
