"""
Test Data Service (API Gateway) Methods
"""
import datetime
import json
from time import mktime
import uuid

from .conftest import create_test_cases


# HTTP Status Codes considered as OK
HTTPS_OK_CODES = [200, 201]
HTTPS_NOT_OK_CODES = [400]


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
    bucket_testpath = 'pytest_methods_{}'.format(str(uuid.uuid4()))

    apig_id = aws_settings['aws_restapiid']
    bucket = aws_settings['aws_s3']

    # Retrieve info of all resources
    resp = apig_client.get_resources(restApiId=apig_id, limit=25)
    ret = resp['ResponseMetadata']['HTTPStatusCode'] in HTTPS_OK_CODES
    if ret is False:
        print('Response:\n{}'.format(json.dumps(resp, cls=DefaultEncoder, indent=2)))
    assert ret

    ###########################################################################
    # Expected 1 resource: `item` and 2 items including '/'
    expected_items = {
        '/':'',
        '/item':''
    }
    assert len(resp['items']) == len(expected_items.items())

    for item in resp['items']:
        assert item['path'] in expected_items.keys()
        expected_items[item['path']] = item['id']

    ###########################################################################
    # Test each resource and its methods

    test_cases = create_test_cases(bucket, sample_test_file, bucket_testpath)

    # NOTES: Need an empty headers
    #   Known issue: Internal Server Error Only When Testing Invoke Method via AWS API
    #   https://forums.aws.amazon.com/thread.jspa?threadID=248714&tstart=0
    for test_case in test_cases:
        print("Testing {} {}".format(test_case['method'], test_case['querystr']))

        resp = apig_client.test_invoke_method(
            restApiId=apig_id,
            resourceId=expected_items['/item'],
            httpMethod=test_case['method'],
            pathWithQueryString=test_case['querystr'],
            headers={},
            body=test_case['body'],
            stageVariables={'bucket': bucket}
        )

        ret = resp['status'] in HTTPS_OK_CODES if test_case['pass'] else HTTPS_NOT_OK_CODES
        if ret is False:
            print('Response:\n{}'.format(json.dumps(resp, cls=DefaultEncoder, indent=2)))
        assert ret
