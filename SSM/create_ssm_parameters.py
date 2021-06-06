import boto3

AWS_REGION = "ap-southeast-2"
DATA = {
    "token": None,  # slack verification token
    "client_id": None,  # optional: for app sharing with oauth 2.0
    "client_secret": None,  # optional: for app sharing with oauth 2.0
}
PARAMETER_KEY_PREFIX = "/apps/slack_app/k_cdk_api"
SLACK_APP_NAME = "K-CDK-SlackApp"
#key_id = "TODO The KMS Key ID (optional)"


def create_parameter(name, value):
    resp = boto3.client("ssm", region_name=AWS_REGION).put_parameter(
        Name=f"{PARAMETER_KEY_PREFIX}/{name}",
        Description=f"{SLACK_APP_NAME} {name}",
        Value=value,
        Type="SecureString",
        #KeyId=key_id,
        Tags=[
            {
                "Key": "Billing",
                "Value": SLACK_APP_NAME,
            }
        ],
    )
    print(resp)


for key, value in DATA.items():
    if value:
        create_parameter(key, value)
