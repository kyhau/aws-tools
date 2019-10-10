import boto3
from boto3.session import Session
import logging

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)
logging.info(f"boto3.__version__: {boto3.__version__}")

AWS_PROFILE="default"
AWS_DEFAULT_REGION="ap-southeast-2"


################################################################################
# Entry point

def main():
    session = Session(profile_name=AWS_PROFILE)
    this_identity = session.client("sts").get_caller_identity()
    print(f"Started processing identity {this_identity['Arn']}")


if __name__ == "__main__": main()
