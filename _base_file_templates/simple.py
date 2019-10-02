import boto3
from boto3.session import Session

AWS_PROFILE="default"
AWS_DEFAULT_REGION="ap-southeast-2"


################################################################################
# Entry point

def main():
    session = Session(profile_name=AWS_PROFILE)
    this_identity = session.client("sts").get_caller_identity()
    print(f"Started processing identity {this_identity['Arn']}")


if __name__ == "__main__": main()
