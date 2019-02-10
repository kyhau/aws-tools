from click.testing import CliRunner
from os import makedirs
from os.path import join
import pytest
from zipfile import ZipFile

from arki.aws.lambda_deploy import lambda_deploy
from arki.tests.conftest import write_file


@pytest.fixture
def sample_lambda_deploy_toml(unittest_workspace):
    context = """
[DummyFunction]
'aws.lambda.name' = 'DummyFunction'
'aws.lambda.handler' = 'DummyFunction.lambda_handler'
'aws.lambda.region' = 'ap-southeast-2'
'aws.lambda.role.arn' = 'arn:aws:iam::111111111111:role/DummyFunction-Lambda-ExecuteRole'
'aws.lambda.runtime' = 'python3.6'
'aws.lambda.memory' = 2048
'aws.lambda.timeout' = 60
'aws.lambda.kmskey.arn' = ''
'aws.lambda.environment' = {'x1' = 'v1', 'x2' = 'v2'}

[DummyFunction.dev]
'aws.lambda.alias' = 'DEV'

[DummyFunction.staging]
'aws.lambda.alias' = 'STAGING'

[DummyFunction.v1]
'aws.lambda.alias' = 'V1'
    """
    return write_file(unittest_workspace, "test_lambda_deploy_1.toml", context)


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
def mock_lambda_update_function_code(mock_boto3_client):
    update_function_code = mock_boto3_client("lambda", "ap-southeast-2").update_function_code
    update_function_code.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 200},
        "Version": "dummy-version-123",
        "RevisionId": "dummy-rid-123"
    }
    return update_function_code


@pytest.fixture
def mock_lambda_update_function_configuration(mock_boto3_client):
    update_function_configuration = mock_boto3_client("lambda", "ap-southeast-2").update_function_configuration
    update_function_configuration.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 200},
        "Version": "dummy-version-123",
        "RevisionId": "dummy-rid-123"
    }
    return update_function_configuration


@pytest.fixture
def mock_lambda_update_alias(mock_boto3_client):
    update_alias = mock_boto3_client("lambda", "ap-southeast-2").update_alias
    update_alias.return_value = {
        "ResponseMetadata": {"HTTPStatusCode": 200},
        "FunctionVersion": "dummy-version-123",
        "AliasArn": "dummy-alias-arn"
    }
    return update_alias


def test_lambda_deploy_passed(
        sample_lambda_deploy_toml,
        dummy_lambda_zip,
        mock_lambda_update_function_code,
        mock_lambda_update_function_configuration,
        mock_lambda_update_alias
):
    args = [
        "-z", dummy_lambda_zip,
        "-d", "Unit test description",
        "-s", "DummyFunction.dev",
        sample_lambda_deploy_toml,
    ]

    print("CgeckPtasdad khdakjndkadhahfkajd")

    runner = CliRunner()
    result = runner.invoke(lambda_deploy, args)
    assert result.exit_code == 0

    mock_lambda_update_function_configuration.assert_any_call(
        Description="Unit test description",
        Environment={"Variables": {"x1": "v1", "x2": "v2"}},
        FunctionName="DummyFunction",
        Handler="DummyFunction.lambda_handler",
        MemorySize=2048,
        Role="arn:aws:iam::111111111111:role/DummyFunction-Lambda-ExecuteRole",
        Runtime="python3.6",
        Timeout=60
    )

    mock_lambda_update_alias.assert_any_call(
        FunctionName="DummyFunction",
        Name="DEV",
        FunctionVersion="dummy-version-123",
        Description="Unit test description",
    )

