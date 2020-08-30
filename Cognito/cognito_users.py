"""
List users of a User Pool
"""
import boto3
import click


def list_all_users(userpool_id):
    user_list = []

    client = boto3.client("cognito-idp")
    params = {"UserPoolId": userpool_id}
    for page in client.get_paginator('list_users').paginate(**params).result_key_iters():
        for item in page:
            user_list.append(item)

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
    print(f"Total number of users: {len(user_list)}")


@click.command()
@click.argument("userpoolid")
def main(userpoolid):
    users = list_all_users(userpoolid)
    print_users(users)


if __name__ == "__main__":
     main()
