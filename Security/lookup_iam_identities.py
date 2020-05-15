"""
Given a user profile, look up what linked IAM identities it has,
"""
import boto3
from boto3.session import Session
import click
from collections import defaultdict
import json
import logging
from os.path import basename


APP_NAME = basename(__file__).split(".")[0]
DEFAULT_SESSION_NAME = "AssumeRoleSession-ListIamUsers-local"
OUTPUT_FILE = f"{APP_NAME}.json"

logging.getLogger().setLevel(logging.DEBUG)


class ResultSet:
    def __init__(self):
        self.data = defaultdict(lambda: defaultdict(dict))
        """
        {
            account_id: {
                user_arn: {
                    "AttachedInlinePolicies": {
                      string(policy arn): [ 
                          { "Action": ... },
                      ],
                    },
                    "AttachedManagedPolicies": {}
                    "Groups": [],
                    "Roles": [],
                    "UserId": string,
                },
                role_arn: {
                    "AttachedInlinePolicies": {},
                    "AttachedManagedPolicies": {}.
                    "UserId": string,
                },
            },
        }
        """

    def __del__(self):
        """Print data to file"""
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2, sort_keys=True)
        logging.info(f"Output file: {OUTPUT_FILE}")


def assume_role(role_arn, session_name="AssumeRoleSession1", duration_secs=3600):
    resp = boto3.client("sts").assume_role(
        RoleArn=role_arn,
        RoleSessionName=session_name,
        DurationSeconds=duration_secs,  # 15 mins to 1 hour or 12 hours
    )
    return Session(
        aws_access_key_id=resp["Credentials"]["AccessKeyId"],
        aws_secret_access_key=resp["Credentials"]["SecretAccessKey"],
        aws_session_token=resp["Credentials"]["SessionToken"]
    )


def process_identity(session, result):
    try:
        # Retrieve aws account id, identity arn, user ID
        this_identity = session.client("sts").get_caller_identity()
        account_id = this_identity["Account"]
        arn = this_identity["Arn"]

        logging.info(f"Started processing identity {arn}")

        result[account_id][arn] = defaultdict(lambda: defaultdict(list))
        result[account_id][arn].update({"UserId": this_identity["UserId"]})

        sub_result = result[account_id][arn]

        iam_client = session.client("iam")

        if f"arn:aws:iam::{account_id}:user/" in arn:
            user_name = arn.split("/")[-1]

            # 1. Retrieve managed policies and inline policies
            retrieve_managed_policy_permissions(sub_result, iam_client, user_name, "user")
            retrieve_inline_policy_permissions(sub_result, iam_client, user_name, "user")

            # 2. Retrieve policies of attached group(s)
            group_names = []
            for group in iam_client.list_groups_for_user(UserName=user_name)["Groups"]:
                logging.info(f"Processing group {group['GroupName']}")
                group_names.append(group["GroupName"])
                retrieve_managed_policy_permissions(sub_result, iam_client, group["GroupName"], "group")
                retrieve_inline_policy_permissions(sub_result, iam_client, group["GroupName"], "group")
            sub_result["Groups"] = group_names

            # 3. Retrieve any allowed assume roles
            role_arns = set()
            for policy_name, statements in sub_result["AttachedInlinePolicies"].items():
                for statement in statements:
                    if statement["Effect"] == "Allow" and "sts:AssumeRole" in statement["Action"]:
                        role_arns.add(statement["Resource"])
            sub_result["Roles"] = list(role_arns)
            for role_arn in role_arns:
                logging.info(f"Processing assume_role {role_arn}")
                session_1 = assume_role(role_arn=role_arn, session_name=DEFAULT_SESSION_NAME)
                process_identity(session_1, result)

        elif f"arn:aws:sts::{account_id}:assumed-role/" in arn:
            role_name = arn.split("/")[-2]

            # Retrieve managed policies and inline policies
            retrieve_managed_policy_permissions(sub_result, iam_client, role_name, "role")
            retrieve_inline_policy_permissions(sub_result, iam_client, role_name, "role")

        elif f"arn:aws:sts::{account_id}:role/" in arn:
            role_name = arn.split("/")[-1]

            # Retrieve managed policies and inline policies
            retrieve_managed_policy_permissions(sub_result, iam_client, role_name, "role")
            retrieve_inline_policy_permissions(sub_result, iam_client, role_name, "role")
        else:
            logging.error(f"TODO: {arn}")

    except Exception as e:
        logging.error(e)


def retrieve_managed_policy_permissions(result, iam_client, name, type):
    if type == "user":
        operation_name = "list_attached_user_policies"
        operation_params = {"UserName": name}
    elif type == "role":
        operation_name = "list_attached_role_policies"
        operation_params = {"RoleName": name}
    else:
        operation_name = "list_attached_group_policies"
        operation_params = {"GroupName": name}

    logging.info("Retrieving managed policies")

    managed_policy_arns = set()
    paginator = iam_client.get_paginator(operation_name)
    for page in paginator.paginate(**operation_params):
        for policy in page["AttachedPolicies"]:
            managed_policy_arns.add(policy["PolicyArn"])

    logging.info("Retrieving policy document of managed policies")

    for managed_policy_arn in managed_policy_arns:
        policy = iam_client.get_policy(PolicyArn=managed_policy_arn)
        policy_version = iam_client.get_policy_version(
            PolicyArn=managed_policy_arn,
            VersionId=policy["Policy"]["DefaultVersionId"]
        )
        result["AttachedManagedPolicies"][managed_policy_arn] = policy_version["PolicyVersion"]["Document"]["Statement"]


def retrieve_inline_policy_permissions(result, iam_client, name, type):
    if type == "user":
        operation_name = "list_user_policies"
        operation_params = {"UserName": name}
        get_policy_func = iam_client.get_user_policy
    elif type == "role":
        operation_name = "list_role_policies"
        operation_params = {"RoleName": name}
        get_policy_func = iam_client.get_role_policy
    else:
        operation_name = "list_group_policies"
        operation_params = {"GroupName": name}
        get_policy_func = iam_client.get_group_policy

    logging.info("Retrieving inline policies")

    inline_policy_names = set()
    paginator = iam_client.get_paginator(operation_name)
    for page in paginator.paginate(**operation_params):
        for policy_name in page["PolicyNames"]:
            inline_policy_names.add(policy_name)

    logging.info("Retrieving policy document of inline policies")

    for inline_policy_name in inline_policy_names:
        operation_params.update({"PolicyName": inline_policy_name})
        policy = get_policy_func(**operation_params)
        result["AttachedInlinePolicies"][inline_policy_name] = policy["PolicyDocument"]["Statement"]


@click.command()
@click.option("--profile", "-p", default="default", help="AWS profile name")
def main(profile):
    result = ResultSet()
    session = Session(profile_name=profile)
    process_identity(session, result.data)


if __name__ == "__main__": main()
