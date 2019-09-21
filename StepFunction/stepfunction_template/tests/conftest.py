import boto3
import logging
import pytest

logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")
logging.getLogger("botocore").setLevel(logging.CRITICAL)


@pytest.fixture(scope="session")
def unittest_configs():
    return {}


@pytest.fixture(scope="session")
def sfn_arn(unittest_configs):
    """ Return the ARN of MyService-StateMachine-Test
    """
    return unittest_configs["aws.statemachine.arn"]


@pytest.fixture(scope="session")
def sfn_client(unittest_configs):
    """ Return an instance of boto3 stepfunctions client
    """
    sfn_region = unittest_configs["aws.stepfunctions.region"]

    return boto3.client("stepfunctions",
        region_name = sfn_region
    )
