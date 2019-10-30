import boto3
import click
import logging
from os.path import basename
from warrant import Cognito

from arki_common.configs import (
    init_wrapper,
    default_config_file_path,
)

APP_NAME = basename(__file__).split(".")[0]

# Default configuration file location
DEFAULT_CONFIG_FILE = default_config_file_path(f"{APP_NAME}.toml")

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


@init_wrapper
def process(*args, **kwargs):
    try:
        settings = kwargs.get("_arki_settings")
        tokens = kwargs.get("tokens")
        list_users = kwargs.get("list_users")

        userpool_id = settings["aws.cognito.userpool.id"]
        userpool_appclientid = settings["aws.cognito.userpool.appclientid"]

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
        return 1

    return 0


@click.command()
@click.argument("config_file", required=False, default=DEFAULT_CONFIG_FILE)
@click.option("--config_section", "-s", required=False, default=APP_NAME, help=f"E.g. {APP_NAME}.staging")
@click.option("--tokens", "-t", required=False, help="Return tokens for user_id:user_password")
@click.option("--list_users", "-l", is_flag=True, help="List all users of a Cognito user pool specified with `section`")
def main(config_file, config_section, tokens, list_users):
    """
    aws_cognito supports getting tokens for a Cognito user and list all users of a User Pool.
    """
    process(
        app_name=APP_NAME,
        config_file=config_file,
        default_configs=DEFAULT_CONFIGS,
        config_section=config_section,
        tokens=tokens,
        list_users=list_users,
    )
