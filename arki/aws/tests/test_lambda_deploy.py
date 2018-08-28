import boto3
from click.testing import CliRunner
from moto import mock_lambda
from os import makedirs
from os.path import join
import pytest
from zipfile import ZipFile

from arki.aws.lambda_deploy import (
    DEFAULT_CONFIGS,
    lambda_deploy,
    prepare_func_configuration_args
)
from arki.configs import read_configs
from arki.tests.conftest import write_file


@pytest.fixture
def sample_lambda_deploy_ini(unittest_workspace):
    context = """
[default]
aws.profile = 
aws.lambda.name = DummyFunction
aws.lambda.handler = DummyFunction.lambda_handler
aws.lambda.region = ap-southeast-2
aws.lambda.role.arn = arn:aws:iam::111111111111:role/DummyFunction-Lambda-ExecuteRole
aws.lambda.runtime = python3.6
aws.lambda.memory = 2048
aws.lambda.timeout = 60
aws.lambda.kmskey.arn =
aws.lambda.environment =
  x1: v1
  x2: v2

[dev]
aws.lambda.alias = DEV

[staging]
aws.lambda.alias = STAGING

[v1]
aws.lambda.alias = V1
    """
    return write_file(unittest_workspace, "test_lambda_deploy_1.ini", context)


@pytest.fixture(scope="session")
def dummy_lambda_zip(unittest_workspace):
    pfunc = """
def lambda_handler(event, context):
    print("dummy_lambda success")
    return event
    """
    test_dir = join(unittest_workspace, "lambda_deploy")
    makedirs(test_dir)

    func_file = write_file(test_dir, "lambda_function.py", pfunc)
    func_zip = join(test_dir, "DummyFunction.zip")

    with ZipFile(func_zip, "w") as fz:
        fz.write(func_file, arcname="lambda_function.py")

    return func_zip


@pytest.fixture
def mock_sample_lambda(dummy_lambda_zip, sample_lambda_deploy_ini):
    """Mock lambda service with moto
    """
    with mock_lambda():
        client = boto3.client("lambda")

        with open(dummy_lambda_zip, mode="rb") as fh:
            byte_stream = fh.read()

        settings = read_configs(
            ini_file=sample_lambda_deploy_ini,
            config_dict=DEFAULT_CONFIGS,
            section_list=["dev"]
        )

        args = prepare_func_configuration_args(settings, "Unit test init DummyLambda")
        args["Code"] = { "ZipFile": byte_stream}

        ret = client.create_function(**args)

        import json
        json.dumps(ret)

        yield client



def todo_test_lambda_deploy_failed(mock_sample_lambda, sample_lambda_deploy_ini, dummy_lambda_zip):
    args = [
        "-z", dummy_lambda_zip,
        "-a", "dev",
        "-d", "Unit test description",
        sample_lambda_deploy_ini,
    ]
    runner = CliRunner()
    result = runner.invoke(lambda_deploy, args)
    assert result.exit_code == 1

