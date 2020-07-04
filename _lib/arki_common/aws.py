from boto3.session import Session
from botocore.exceptions import ClientError
import logging
from time import time


class AwsApiHelper():
    AUTH_ERRORS = [
        "AccessDenied", "AccessDeniedException", "AuthFailure",
        "UnauthorizedOperation", "UnrecognizedClientException"
    ]
    CRED_ERRORS = ["ExpiredToken", "InvalidClientTokenId"]
    
    def __init__(self):
        """Update the root logger to get messages at DEBUG and above"""
        logging.getLogger("botocore").setLevel(logging.CRITICAL)
        logging.getLogger("boto3").setLevel(logging.CRITICAL)
        logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)

    @staticmethod
    def paginate(client, func_name, kwargs=None):
        for page in client.get_paginator(func_name).paginate(**kwargs if kwargs else {}).result_key_iters():
            for item in page:
                yield item

    def process_account(self, session, account_id, aws_region, service, kwargs):
        """Process the request at the specified region or all regions"""
        regions = session.get_available_regions(service) \
            if aws_region is None or aws_region.lower() == "all" else [aws_region]
        for region in regions:
            logging.debug(f"Checking {account_id} {region}")
            try:
                if self.process_request(session, account_id, region, kwargs) is not None:
                    return True
            except ClientError as e:
                self.process_client_error(e, account_id, region)
            except Exception:
                import traceback
                traceback.print_exc()

    def process_client_error(self, e, account_id, region):
        error_code = e.response["Error"]["Code"]
        if error_code in AwsApiHelper.AUTH_ERRORS:
            logging.warning(f"Unable to process {account_id} {region}: {error_code}")
        else:
            raise

    def process_request(self, session, account_id, region, kwargs):
        """Process request for a region of an account"""
        pass
    
    def post_process(self):
        pass

    def start(self, profile, region, service, kwargs=None):
        start = time()
        try:
            for (session, account_id, profile_name) in MultiAccountHelper().sessions(profile):
                if self.process_account(session, account_id, region, service, kwargs) is not None:
                    break
            self.post_process()
        finally:
            logging.info(f"Total execution time: {time() - start}s")


class MultiAccountHelper():
    def __init__(self):
        self._accounts_processed = []

    @staticmethod
    def read_aws_profile_names():
        from configparser import ConfigParser
        from os.path import expanduser, join
        try:
            cp = ConfigParser()
            cp.read(join(expanduser("~"), ".aws", "credentials"))
            return cp.sections()
        except Exception as e:
            logging.error(e)

    def sessions(self, profile):
        for profile_name in [profile] if profile else self.read_aws_profile_names():
            try:
                session = Session(profile_name=profile_name)
                account_id = session.client("sts").get_caller_identity()["Account"]
                if account_id not in self._accounts_processed:
                    self._accounts_processed.append(account_id)
                    yield (session, account_id, profile_name)
            except ClientError as e:
                if e.response["Error"]["Code"] in AwsApiHelper.CRED_ERRORS:
                    logging.warning(f'{profile_name} {e.response["Error"]["Code"]}. Skipped')
                else:
                    raise


def assume_role(role_arn, session_name="AssumeRoleSession1", duration_secs=3600):
    import boto3
    resp = boto3.client("sts").assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name,
        DurationSeconds=duration_secs,  # 15 mins to 1 hour or 12 hours
    )
    return Session(
        aws_access_key_id=resp["Credentials"]["AccessKeyId"],
        aws_secret_access_key=resp["Credentials"]["SecretAccessKey"],
        aws_session_token=resp["Credentials"]["SessionToken"]
    )


def get_tag_value(tags, key="Name"):
    for tag in tags:
        if tag["Key"] == key:
            return tag["Value"]
    return ""
