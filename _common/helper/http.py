import logging
from .ser import dump_json

# HTTP Status Codes considered as OK
HTTPS_OK_CODES = [200, 201, 202]


def check_response(resp):
    """Check response and log message if needed"""
    ret = resp["ResponseMetadata"]["HTTPStatusCode"] in HTTPS_OK_CODES
    if ret is False:
        logging.error(f"Response:\n{dump_json(resp)}")
    return ret
