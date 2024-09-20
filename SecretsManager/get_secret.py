import boto3
import base64
from botocore.exceptions import ClientError
import click

# See https://docs.aws.amazon.com/code-samples/latest/catalog/python-secretsmanager-secrets_manager.py.html
# See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html


def get_secret(secret_name, region_name, profile):
    client = boto3.session.Session(profile_name=profile).client("secretsmanager", region_name=region_name)
    
    try:
        resp = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            # Secrets Manager can"t decrypt the protected secret text using the provided KMS key.
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            # An error occurred on the server side.
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            # You provided an invalid value for a parameter.
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            # You provided a parameter value that is not valid for the current state of the resource.
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            # We can"t find the resource that you asked for.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if "SecretString" in resp:
            secret = resp["SecretString"]
        else:
            secret = base64.b64decode(resp["SecretBinary"])

        return secret


@click.command()
@click.option("--secret_name", "-s", required=True, help="Secret name")
@click.option("--profile", "-p", default="default", help="AWS profile name")
@click.option("--region", "-r", default="ap-southeast-2", help="AWS region")
def main(secret_name, profile, region):
    print(get_secret(secret_name, region, profile))


if __name__ == "__main__": main()
