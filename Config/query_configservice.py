from boto3.session import Session
import click

from arki_common.utils import print_json


def list_action(session, sql_statement):
    account_id = session.client("sts").get_caller_identity()["Account"]

    for region in session.get_available_regions("config"):
        if region != "ap-southeast-2":
            continue
        print(f"Checking {account_id} {region}")

        client = session.client("config", region_name=region)
        resp = client.select_resource_config(Expression=sql_statement)
        next_token = resp["NextToken"]
        print_json(resp["Results"])
        while next_token:
            resp = client.select_resource_config(Expression=sql_statement, NextToken=next_token)
            next_token = resp.get("NextToken")
            print_json(resp["Results"])


@click.command()
@click.option("--profile", "-p", default="default", help="AWS profile name")
@click.option("--profilesfile", "-f", help="File containing AWS profile names")
@click.option("--sqlfile", "-s", required=True, help="File containing the sql statement")
def main(profile, profilesfile, sqlfile):
    
    with open(sqlfile, "r") as f:
        sql_statement = f.read()

    if profilesfile:
        with open(profilesfile, "r") as f:
            profile_names = f.readlines()
    else:
        profile_names = [profile]
    
    for profile_name in profile_names:
        session = Session(profile_name=profile_name.strip())
        list_action(session, sql_statement)


if __name__ == "__main__": main()
