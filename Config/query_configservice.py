from boto3.session import Session
import click

from arki_common.aws import assume_role, read_role_arns_from_file
from arki_common.utils import print_json


def read_file(filename):
    with open(filename, "r") as f:
        return f.read()


def dump(data, output_filename, append=True, to_console=True):
    if to_console is True:
        print(data)

    with open(output_filename, "a" if append else "w") as f:
        f.write(f'{",".join(list(map(str, data)))}\n')


def list_action(session, sql_statement):
    account_id = session.client("sts").get_caller_identity()["Account"]

    for region in session.get_available_regions("ec2"):
        if region != "ap-southeast-2":
            continue
        print(f"Checking {account_id} {region}")

        client = session.client("config", region_name=region)
        paginator = client.get_paginator("select_resource_config")
        for page in paginator.paginate(
            Expression=sql_statement,
        ):
            print_json(page)
            

################################################################################
# Entry point

@click.command()
@click.option("--profile", "-p", default="default", help="AWS profile name")
@click.option("--rolesfile", "-f", help="File containing Role ARNs")
@click.option("--sqlfile", "-s", required=True, help="File containing the sql statement")
def main(profile, rolesfile, sqlfile):
    
    sql_statement = read_file(sqlfile)
    
    if rolesfile:
        for role_arn, acc_name in read_role_arns_from_file(filename=rolesfile):
            session = assume_role(role_arn=role_arn)
            list_action(session, sql_statement)
    else:
        session = Session(profile_name=profile)
        list_action(session, sql_statement)


if __name__ == "__main__": main()
