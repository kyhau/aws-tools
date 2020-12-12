# Simple function for testing private API Gateway
# @author kyhau
import json
import logging
import os

import urllib3

API_PATH = os.environ.get("API_PATH", "/v0/mock")
APIGW_ENDPOINT = os.environ.get("APIGW_ENDPOINT")
APIGW_VPCE_R53_Alias = os.environ.get("APIGW_VPCE_R53_Alias")
VPCE_PUBLIC_DNS_NAME = os.environ.get("VPCE_PUBLIC_DNS_NAME")
passed = 0
failed = 0

logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

http = urllib3.PoolManager()


def test_url(url, headers={}):
    global passed, failed
    try:
        resp = http.request("POST", url, headers=headers)
        data = json.loads(resp.data.decode("utf-8"))
        print(f"Response: {data}")
        if data.get("message") == "OK":
            passed += 1
        else:
            failed += 1
    except Exception as e:
        print(f"Error: {e}")
        failed += 1


def lambda_handler(event, context):

    if APIGW_ENDPOINT:
        # Default APIGW endpoint; work only if private DNS enabled for your interface endpoint.
        default_apigw_endpoint_url = f"https://{APIGW_ENDPOINT}{API_PATH}"
        print(f"Testing default APIGW endpoint (work only if private DNS enabled): {default_apigw_endpoint_url}")
        test_url(default_apigw_endpoint_url)

    if APIGW_VPCE_R53_Alias:
        # API Gateway Route 53 Alias for VPC endpoint associated
        apigw_vpce_dns_url = f"https://{APIGW_VPCE_R53_Alias}{API_PATH}"
        print(f"Testing API Gateway Route 53 Alias for VPC endpoint associated: {apigw_vpce_dns_url}")
        test_url(apigw_vpce_dns_url)

    if VPCE_PUBLIC_DNS_NAME and APIGW_ENDPOINT:
        public_dns_url = f"https://{VPCE_PUBLIC_DNS_NAME}{API_PATH}"

        # Public DNS name with a Host header
        print(f"Testing {public_dns_url} with headers Host={APIGW_ENDPOINT}")
        test_url(public_dns_url, headers={"Host": APIGW_ENDPOINT})

        # Public DNS name with the x-apigw-api-id header
        API_ID = APIGW_ENDPOINT.split(".")[0]
        print(f"Testing {public_dns_url} with headers x-apigw-api-id={API_ID}")
        test_url(public_dns_url, headers={"x-apigw-api-id": API_ID})

    return {
        "body": json.dumps({"passed": passed, "failed": failed}),
        "headers": {"Content-Type": "application/json"},
        "statusCode": 200,
    }
