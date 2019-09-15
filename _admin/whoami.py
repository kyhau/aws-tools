"""
Who am I?
"""
from boto3.session import Session
import click
from collections import defaultdict
import logging

from arki_common.aws import assume_role, read_role_arns_from_file, DEFAULT_ROLE_ARNS_FILE
from arki_common.utils import print_json


logFormatter = logging.Formatter("%(message)s")
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

fileHandler = logging.FileHandler("whoami.txt")
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)

DEFAULT_SESSION_NAME = "AssumeRoleSession-WhoAmI-local"

results = defaultdict(lambda: defaultdict(list))
#results["user_arn"]["ALLOW"].append("permission")


def list_action(session):
    try:
        # 1. Retrieve aws account id, identity arn, user ID
        this_identity = session.client("sts").get_caller_identity()
        for key in ["Account", "Arn", "UserId"]:
            results[key] = this_identity[key]

        account_id = this_identity["Account"]
        arn = this_identity["Arn"]

        iam_client = session.client("iam")

        if f"arn:aws:iam::{account_id}:user/" in arn:
            user_name = arn.split("/")[-1]

            # 1. Retrieve managed policies and inline policies
            retrieve_managed_policy_permissions(iam_client, user_name, "user")
            retrieve_inline_policy_permissions(iam_client, user_name, "user")

            # 2. Retrieve policies of attached group(s)
            group_names = []
            for group in iam_client.list_groups_for_user(UserName=user_name)["Groups"]:
                group_names.append(group["GroupName"])
                retrieve_managed_policy_permissions(iam_client, group["GroupName"], "group")
                retrieve_inline_policy_permissions(iam_client, group["GroupName"], "group")
            results["Groups"] = group_names

            # 3. Retrieve any allowed assume roles
            role_arns = set()
            for policy_name, statements in results["AttachedInlinePolicies"].items():
                for statement in statements:
                    if statement["Effect"] == "Allow" and "sts:AssumeRole" in statement["Action"]:
                        role_arns.add(statement["Resource"])
            results["Roles"] = list(role_arns)
            for role_arn in role_arns:
                session_1 = assume_role(role_arn=role_arn, session_name=DEFAULT_SESSION_NAME)
                list_action(session_1)

        elif f"arn:aws:sts::{account_id}:assumed-role/" in arn:
            role_name = arn.split("/")[-2]

            # Retrieve managed policies and inline policies
            retrieve_managed_policy_permissions(iam_client, role_name, "role")
            retrieve_inline_policy_permissions(iam_client, role_name, "role")

        elif f"arn:aws:sts::{account_id}:role/" in arn:
            role_name = arn.split("/")[-1]

            # Retrieve managed policies and inline policies
            retrieve_managed_policy_permissions(iam_client, role_name, "role")
            retrieve_inline_policy_permissions(iam_client, role_name, "role")
        else:
            rootLogger.error(f"TODO: {arn}")
    except Exception as e:
        rootLogger.error(e)


def retrieve_managed_policy_permissions(iam_client, name, type):
    if type == "user":
        operation_name = "list_attached_user_policies"
        operation_params = {"UserName": name}
    elif type == "role":
        operation_name = "list_attached_role_policies"
        operation_params = {"RoleName": name}
    else:
        operation_name = "list_attached_group_policies"
        operation_params = {"GroupName": name}

    managed_policy_arns = set()
    paginator = iam_client.get_paginator(operation_name)
    for page in paginator.paginate(**operation_params):
        for policy in page["AttachedPolicies"]:
            managed_policy_arns.add(policy["PolicyArn"])

    for managed_policy_arn in managed_policy_arns:
        policy = iam_client.get_policy(PolicyArn=managed_policy_arn)
        policy_version = iam_client.get_policy_version(
            PolicyArn=managed_policy_arn,
            VersionId=policy["Policy"]["DefaultVersionId"]
        )
        results["AttachedManagedPolicies"][managed_policy_arn] = policy_version["PolicyVersion"]["Document"]["Statement"]


def retrieve_inline_policy_permissions(iam_client, name, type):
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

    inline_policy_names = set()
    paginator = iam_client.get_paginator(operation_name)
    for page in paginator.paginate(**operation_params):
        for policy_name in page["PolicyNames"]:
            inline_policy_names.add(policy_name)

    for inline_policy_name in inline_policy_names:
        operation_params.update({"PolicyName": inline_policy_name})
        policy = get_policy_func(**operation_params)
        results["AttachedInlinePolicies"][inline_policy_name] = policy["PolicyDocument"]["Statement"]


################################################################################
# Entry point

@click.command()
@click.option("--profile", "-p", default="default", help="AWS profile name")
def main(profile):
    session = Session(profile_name=profile)
    list_action(session)

    #for role_arn in read_role_arns_from_file(filename=DEFAULT_ROLE_ARNS_FILE):
    #    session = assume_role(role_arn=role_arn, session_name=DEFAULT_SESSION_NAME)
    #    list_action(session)

    print_json(results, rootLogger)


if __name__ == "__main__": main()
