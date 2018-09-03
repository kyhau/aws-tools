import boto3
import click
import logging
from os.path import join
import sys
from warrant import Cognito
from arki.aws.base_helper import BaseHelper
from arki.configs import ARKI_LOCAL_STORE_ROOT


# Default configuration file location
ENV_STORE_FILE = join(ARKI_LOCAL_STORE_ROOT, "cognito.ini")

DEFAULT_CONFIGS = {
    "aws.profile": {"required": True},
    "aws.cognito.userpool.appclientid": {"required": True},
    "aws.cognito.userpool.id": {"required": True},
    "aws.cognito.userpool.region": {"required": True, "default": "ap-southeast-2"},
}


def authenticate(userpool_id, userpool_appclientid, username, userpass):
    """
    Authenticate a user and return id_token, refresh_token, access_token.

    :param userpool_id: Userpool ID
    :param userpool_appclientid: Userpool applcation client ID
    :param username: Cognito user login
    :param userpass: Cognito user password
    :return: id_token, refresh_token, access_token
    """
    user = Cognito(userpool_id, userpool_appclientid, username=username)
    user.authenticate(password=userpass)
    return {
        "access_token": user.access_token,
        "id_token": user.id_token,
        "refresh_token": user.refresh_token,
    }


def list_all_users(userpool_id):
    """
    List all users

    :param userpool_id: Userpool ID
    :return: List of users
    """
    client = boto3.client("cognito-idp")

    # Max Limit=60
    resp = client.list_users(UserPoolId=userpool_id)
    user_list = resp["Users"]
    page_token = resp.get("PaginationToken")

    while page_token:
        resp = client.list_users(UserPoolId=userpool_id, PaginationToken=page_token)
        user_list.extend(resp["Users"])
        page_token = resp.get("PaginationToken")

    return user_list


def print_users(user_list):
    lines = ["# Username, Enabled, UserStatus, UserCreateDate, UserLastModifiedDate, given_name, family_name"]

    for u in user_list:
        data = [
            u["Username"],
            "Enabled" if u["Enabled"] is True else "Disabled",
            u["UserStatus"],
            u["UserCreateDate"].strftime("%Y-%m-%d-%H:%M"),
            u["UserLastModifiedDate"].strftime("%Y-%m-%d-%H:%M"),
        ]
        for a in u["Attributes"]:
            if a["Name"] in ["given_name", "family_name"]:
                data.append(a["Value"])
        lines.append(f'{", ".join(data)}')

    for line in lines:
        print(line)
    print(f"Total users: {len(user_list)}")


@click.command()
@click.argument("ini_file", required=False, default=ENV_STORE_FILE)
@click.option("--init", "-i", is_flag=True, help="Set up new configuration")
@click.option("--section", "-s", required=False, default="prod", help="Choices: [dev, prod], default=prod")
@click.option("--tokens", "-t", required=False, help="Return tokens for user_id:user_password")
@click.option("--list_users", "-l", is_flag=True, help="List all users of a Cognito user pool specified with `section`")
def main(ini_file, init, section, tokens, list_users):
    """
    aws_cognito supports getting tokens for a Cognito user and list all users of a User Pool.

    Use --init to create a `ini_file` with the default template to start.
    """

    try:
        helper = BaseHelper(DEFAULT_CONFIGS, ini_file, stage_section=section)

        if init:
            helper._create_ini_template(module=__file__, allow_overriding_default=True)
        else:
            userpool_id = helper.settings["aws.cognito.userpool.id"]
            userpool_appclientid = helper.settings["aws.cognito.userpool.appclientid"]

            if tokens:
                data = tokens.split(":")
                uname = data[0].strip().lower()
                upass = data[1].strip()

                ret_tokens = authenticate(userpool_id, userpool_appclientid, uname, upass)
                for token_name, token in ret_tokens.items():
                    print(f"{token_name}:\n{token}\n")

            if list_users:
                user_list = list_all_users(userpool_id)
                print_users(user_list)

    except Exception as e:
        logging.error(e)
        sys.exit(1)

    sys.exit(0)
