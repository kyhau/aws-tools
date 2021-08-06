"""
Calling admin_initiate_auth with OAuth2 hash

Return
{
    'ChallengeName': 'SMS_MFA'|'SOFTWARE_TOKEN_MFA'|'SELECT_MFA_TYPE'|'MFA_SETUP'|'PASSWORD_VERIFIER'|'CUSTOM_CHALLENGE'|'DEVICE_SRP_AUTH'|'DEVICE_PASSWORD_VERIFIER'|'ADMIN_NO_SRP_AUTH'|'NEW_PASSWORD_REQUIRED',
    'Session': 'string',
    'ChallengeParameters': {
        'string': 'string'
    },
    'AuthenticationResult': {
        'AccessToken': 'string',
        'ExpiresIn': 123,
        'TokenType': 'string',
        'RefreshToken': 'string',
        'IdToken': 'string',
        'NewDeviceMetadata': {
            'DeviceKey': 'string',
            'DeviceGroupKey': 'string'
        }
    }
}
"""
import base64
import hashlib
import hmac
import json

import boto3
import click


def oauth2_hash(client_id, client_secret, username):
    """Generate hash - works with user pools that have secrets"""
    try:
        message = bytes(username + client_id, "utf-8")
        key = bytes(client_secret, "utf-8")

        secret_hash = base64.b64encode(hmac.new(key, message, digestmod=hashlib.sha256).digest()).decode()

        print(f"SECRET HASH: {secret_hash}")

    except Exception as e:
        print(f"Error: {e}")


def admin_initiate_auth(client_id, userpool_id, uname, upass, uhash):
    return boto3.client("cognito-idp").admin_initiate_auth(
        AuthFlow="ADMIN_NO_SRP_AUTH",
        AuthParameters={
            "USERNAME": uname,
            "PASSWORD": upass,
            "SECRET_HASH": uhash,
        },
        ClientId=client_id,
        UserPoolId=userpool_id,
    )


@click.command(help="Calling admin_initiate_auth with OAuth2 hash")
@click.option("--client-id", "-i", help="App Client ID")
@click.option("--client-secret", "-s", help="App Client Secret")
@click.option("--username", "-n", help="Cognito User Name")
@click.option("--userpool-id", "-u", help="Cognito User Pool ID")
def main(client_id, client_secret, username, userpool_id):
    upass = click.prompt("Cognito User Password")

    uhash = oauth2_hash(client_id, client_secret, username)

    auth_resp = admin_initiate_auth(client_id, userpool_id, username, upass, uhash)
    print(json.dumps(auth_resp, indent=2))


if __name__ == "__main__":
     main()

