"""
Authenticate a user and return id_token, refresh_token, access_token.
"""
import json

import click
from pycognito import Cognito


@click.command(help="Authenticate a Cognito user and export the token in an output file.")
@click.option("--appclientid", "-a", required=True, help="Userpool application client ID")
@click.option("--username", "-n", required=True, help="Cognito user login")
@click.option("--userpoolid", "-u", required=True, help="Cognito Userpool ID")
@click.option('--password', prompt=True, confirmation_prompt=False, hide_input=True, help="Cognito user password")
def authenticate(appclientid, username, userpoolid, password):
    """
    Authenticate a user and return id_token, refresh_token, access_token.

    :param appclientid: Userpool application client ID
    :param username: Cognito user login
    :param userpoolid: Userpool ID
    :param password: Cognito user password
    :return: id_token, refresh_token, access_token
    """
    user = Cognito(userpoolid, appclientid, username=username)
    user.authenticate(password=password)
    data = {
        "access_token": user.access_token,
        "id_token": user.id_token,
        "refresh_token": user.refresh_token,
    }
    print(data)
    print("Written to tmp_token.json")
    with open("tmp_token.json", "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
     authenticate()
