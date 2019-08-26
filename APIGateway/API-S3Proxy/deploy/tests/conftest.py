"""
conftest.py
"""
import boto3
import configparser
import json
import os
from os.path import dirname, exists, join, realpath
import py.test
from shutil import rmtree
from tempfile import mkdtemp


###############################################################################
# py.test options and env variables

ENV_AWS_ACCESS_KEY_ID = 'aws_access_key_id'
ENV_AWS_SECRET_ACCESS_KEY = 'aws_secret_access_key'

# Environment variable for specifying the specific stage of the API to be tested
ENV_STAGE = 'api_stage'


SETTINGS = {
    'api_json_file': join(dirname(dirname(dirname(dirname(realpath(__file__))))), 'api', 'DataServiceAPI_swagger.json'),
    'aws_region': 'ap-southeast-2',
    'ini_file': join(dirname(dirname(realpath(__file__))), 'aws.ini'),
    'api_stage': 'stage'
}

###############################################################################
# py.test fixtures

@py.test.fixture(scope='module')
def config():
    config = configparser.ConfigParser()
    config.read(SETTINGS['ini_file'])
    return config


@py.test.fixture(scope='module')
def aws_settings(config):
    """Retrieve AWS resource settings from the ini file and environment variables.
    """
    settings = SETTINGS
    settings['aws_restapiid'] = config['default']['aws.apigateway.restApiId']
    settings['aws_s3'] = config['test']['aws.s3']

    settings['aws_access_key_id'] = os.environ[ENV_AWS_ACCESS_KEY_ID]
    settings['aws_secret_access_key'] = os.environ[ENV_AWS_SECRET_ACCESS_KEY]
    if ENV_STAGE in os.environ:
        settings['api_stage'] = os.environ[ENV_STAGE]

    return settings


def create_test_cases(bucket, sample_test_file, test_name):

    with open(sample_test_file, 'r') as fp:
        new_data = fp.read()

    testpath = '?key={}'.format(test_name)
    test_file_1 = '{}/{}'.format(testpath,'pytest_1.json')
    test_file_2 = '{}/a/b/{}'.format(testpath, 'pytest_2.json')

    test_cases = [
        # PUT - Pass:add new bucket/file
        {'method': 'PUT', 'querystr': test_file_1, 'body': new_data, 'pass': True},
        # GET - Pass:confirm file added
        {'method': 'GET', 'querystr': test_file_1, 'body': '', 'pass': True},
        # HEAD - Pass:confirm file added
        {'method': 'HEAD', 'querystr': test_file_1, 'body': '', 'pass': True},

        # GET - Pass:confirm file added
        {'method': 'GET', 'querystr': '?key=nonexistobject', 'body': '', 'pass': False},
        # HEAD - Fail:invalid bucket/file
        {'method': 'HEAD', 'querystr': '?key=nonexistobject', 'body': '', 'pass': False},

        # PUT - Pass:add new bucket/folder/folder/file
        {'method': 'PUT', 'querystr': test_file_2, 'body': new_data, 'pass': True},
        # GET - Pass:confirm file added
        {'method': 'GET', 'querystr': test_file_2,'body': '', 'pass': True},

        # PUT - Pass:overwrite bucket/file
        {'method': 'PUT', 'querystr': test_file_1, 'body': 'helloworld', 'pass': True},

        # DELETE - Pass:delete bucket/file
        {'method': 'DELETE', 'querystr': test_file_1, 'body': '', 'pass': True},
        # GET - Pass:confirm file deleted
        {'method': 'GET', 'querystr': test_file_1,'body': '', 'pass': False},

        # DELETE - Pass:delete bucket/folder/folder/file
        {'method': 'DELETE', 'querystr': test_file_2, 'body': '', 'pass': True},
        # GET - Pass:confirm file deleted
        {'method': 'GET', 'querystr': test_file_2,'body': '', 'pass': False},
    ]

    return test_cases

@py.test.fixture(scope='module')
def apig_client(aws_settings):
    return boto3.client(
        'apigateway',
        aws_access_key_id=aws_settings['aws_access_key_id'],
        aws_secret_access_key=aws_settings['aws_secret_access_key'],
        region_name=aws_settings['aws_region']
    )


def stage_settings(config, stage_name, settings):
    """Retrieve stage-specific settings
    """
    profile = stage_name if stage_name in config.sections() else 'test'
    settings['aws.s3'] = config[profile]['aws.s3']
    settings['aws.cacheClusterEnabled'] = True if config[profile]['aws.apigateway.cacheClusterEnabled'].lower() == 'true' else False
    settings['aws.cacheClusterSize'] = config[profile]['aws.apigateway.cacheClusterSize']
    return settings


@py.test.fixture(scope='session')
def unit_tests_tmp_dir(request):
    t = mkdtemp(prefix='data_service_')
    print('Created tmp test dir {}.'.format(t))

    def teardown():
        # delete sample files created for the unit tests
        if exists(t):
            rmtree(t)
            print('Deleted tmp test dir {}.'.format(t))

    request.addfinalizer(teardown)
    return t


@py.test.fixture(scope='session')
def sample_test_file(unit_tests_tmp_dir):
    filename = join(unit_tests_tmp_dir, 'data_service_testfile.json')

    data = {
        "key1": "value1",
        "key2": "value2"
    }

    with open(filename, 'w') as outfile:
        json.dump(data, outfile)

    return filename
