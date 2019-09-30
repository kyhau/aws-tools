import boto3

AWS_PROFILE="default"
AWS_DEFAULT_REGION="ap-southeast-2"

#boto3.setup_default_session(profile_name=AWS_PROFILE)
client = boto3.session.Session(profile_name=AWS_PROFILE).client("cloudformation")
