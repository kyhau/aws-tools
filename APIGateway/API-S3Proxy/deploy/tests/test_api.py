"""
Test the specified stage of the deployed Data Service API
"""
import datetime
import json
from requests_aws4auth import AWS4Auth
import requests
from time import mktime
import uuid

from .conftest import create_test_cases


class DefaultEncoder(json.JSONEncoder):
    """Encode for the json
    """
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        return json.JSONEncoder.default(self, obj)


def test_data_service(apig_client, aws_settings, sample_test_file):
    """Test Data Service resources.
    """
    bucket_testpath = 'pytest_api_{}'.format(str(uuid.uuid4()))

    apig_id = aws_settings['aws_restapiid']
    api_stage = aws_settings['api_stage']
    bucket = aws_settings['aws_s3']
    region = aws_settings['aws_region']

    auth = AWS4Auth(aws_settings['aws_access_key_id'], aws_settings['aws_secret_access_key'], region, 'execute-api')

    base_url = 'https://{}.execute-api.{}.amazonaws.com/{}/item'.format(apig_id, region, api_stage)

    ###########################################################################
    # Test each api route

    test_cases = create_test_cases(bucket, sample_test_file, bucket_testpath)

    for test_case in test_cases:
        url = base_url + test_case['querystr']
        print("Testing {} {}".format(test_case['method'], url))

        resp = requests.request(
            method=test_case['method'],
            url=url,
            auth=auth,
            data=test_case['body'],
            headers={}
        )

        ret = (resp.status_code is requests.codes.ok) == test_case['pass']
        if ret is False:
            print(resp.text)
        assert ret
