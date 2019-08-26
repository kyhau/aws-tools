import argparse
import boto3
import configparser
import datetime
import json
import logging
import os
import sys
from os.path import dirname, join, realpath
from time import mktime


logging.basicConfig(level=logging.WARNING)

ENV_AWS_ACCESS_KEY_ID = 'aws_access_key_id'
ENV_AWS_SECRET_ACCESS_KEY = 'aws_secret_access_key'

# Check mandatory environment variable settings
if ENV_AWS_ACCESS_KEY_ID not in os.environ:
    print('Environment variable {} not set. Aborted.'.format(ENV_AWS_ACCESS_KEY_ID))
    sys.exit(1)

if ENV_AWS_SECRET_ACCESS_KEY not in os.environ:
    print('Environment variable {} not set. Aborted.'.format(ENV_AWS_SECRET_ACCESS_KEY))

SETTINGS = {
    'api_json_file': join(dirname(dirname(dirname(realpath(__file__)))), 'api', 'DataServiceAPI_swagger.json'),
    'aws_access_key_id': os.environ[ENV_AWS_ACCESS_KEY_ID],
    'aws_secret_access_key': os.environ[ENV_AWS_SECRET_ACCESS_KEY],
    'aws_restapiid': '',
    'aws_region': 'ap-southeast-2',
    'aws_s3': '',
    'ini_file': join(dirname(realpath(__file__)), 'aws.ini'),
}

# HTTP Status Codes considered as OK
HTTPS_OK_CODES = [200, 201]


class DefaultEncoder(json.JSONEncoder):
    """Encode for the json
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        return json.JSONEncoder.default(self, obj)


class ApiGatewayHelper():
    def __init__(self, settings):
        """Initialise attributes and apigateway client
        """
        for k, v in settings.items():
            setattr(self, k, v)

        self.client = boto3.client('apigateway',
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key = self.aws_secret_access_key,
            region_name=self.aws_region
        )

    def put_rest_api(self):
        """Reimport api swagger file to AWS api gateway
        """
        # Retrieve content of the api swagger template
        with open(self.api_json_file, 'rb') as fp:
            data = fp.read()

        print("Reimport API swagger file to api gateway [{}] ...".format(self.aws_restapiid))
        resp = self.client.put_rest_api(restApiId=self.aws_restapiid, mode='overwrite', body=data)

        print('Response:\n{}'.format(json.dumps(resp, cls=DefaultEncoder, indent=2)))
        return resp['ResponseMetadata']['HTTPStatusCode'] in HTTPS_OK_CODES

    def create_deployment(self, stage_name, bucket_name, cache_enabled, cache_size):
        """Create or update a deployment stage
        """
        print("Create or update deployment stage [{}] of api gateway [{}] ...".format(stage_name, self.aws_restapiid))
        resp = self.client.create_deployment(
            restApiId=self.aws_restapiid,
            stageName=stage_name,
            stageDescription=stage_name,
            description=stage_name, # TODO a proper description instead of using the stage name
            cacheClusterEnabled=bool(cache_enabled),
            cacheClusterSize=cache_size,
            variables={
                'bucket': bucket_name
            }
        )

        print('Response:\n{}'.format(json.dumps(resp, cls=DefaultEncoder, indent=2)))
        return resp['ResponseMetadata']['HTTPStatusCode'] in HTTPS_OK_CODES


def main():
    # Retrieve what action to be done from command line
    parser = argparse.ArgumentParser(
        description="Reimport the API Swagger template to AWS and run tests. "\
            + "If `deploy` is specified, the program will instead deploy the "\
            + "current rest api to the specified stage and tested."
    )
    parser.add_argument('--deploy', help="Deploy the current rest api to a stage. Choices: [test, stage, prod]")
    args = parser.parse_args(sys.argv[1:])

    # Retrieve AWS resource settings from the ini file
    config = configparser.ConfigParser()
    config.read(SETTINGS['ini_file'])
    SETTINGS['aws_restapiid'] = config['default']['aws.apigateway.restApiId']

    helper = ApiGatewayHelper(SETTINGS)

    if args.deploy is None:
        # Put the restapi to AWS
        if helper.put_rest_api() is False:
            logging.error("Failed to reimport the api swagger file. Aborted")
            return 1
    else:
        # Retrieve stage-specific settings
        stage_name = args.deploy.lower()
        profile = stage_name if stage_name in config.sections() else 'test'
        s3 = config[profile]['aws.s3']
        cache_enabled = True if config[profile]['aws.apigateway.cacheClusterEnabled'].lower() == 'true' else False
        cache_size = config[profile]['aws.apigateway.cacheClusterSize']

        if helper.create_deployment(stage_name, s3, cache_enabled, cache_size) is False:
            logging.error("Failed to create deployment stage. Aborted")
            return 1
    return 0


if __name__ == '__main__':
    """Entry point for running from command line
    """
    sys.exit(main())