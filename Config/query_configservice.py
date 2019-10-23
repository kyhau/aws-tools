from boto3.session import Session
from botocore.exceptions import ClientError
import click
import logging
from os.path import exists
from shutil import rmtree

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3").setLevel(logging.CRITICAL)


def dump(data, output_filename, to_console=True):
    if to_console is True:
        print(data)
    with open(output_filename, "a") as f:
        f.write(f'{data}\n')


def list_action(session, sql_statement, sqlfile):
    account_id = session.client("sts").get_caller_identity()["Account"]
    
    output_filename = f'{account_id}_{sqlfile.replace(".sql", "")}.txt'
    if exists(output_filename):
        rmtree(output_filename)

    for region in session.get_available_regions("config"):
        try:
            if region != "ap-southeast-2":
                continue
            
            logging.debug(f"Checking {account_id} {region}")
    
            client = session.client("config", region_name=region)
            resp = client.select_resource_config(Expression=sql_statement)
            next_token = resp.get("NextToken")
            for item in resp["Results"]:
                dump(item, output_filename)
    
            while next_token:
                resp = client.select_resource_config(Expression=sql_statement, NextToken=next_token)
                next_token = resp.get("NextToken")
                for item in resp["Results"]:
                    dump(item, output_filename)

        except ClientError as e:
            if e.response["Error"]["Code"] == "UnrecognizedClientException":
                logging.warning(f"Unable to process region {region}")
            else:
                raise

@click.command()
@click.option("--profile", "-p", default="default", help="AWS profile name")
@click.option("--profilesfile", "-f", help="File containing AWS profile names")
@click.option("--sqlfile", "-s", required=True, help="File containing the sql statement (.sql)")
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
        list_action(session, sql_statement, sqlfile)


if __name__ == "__main__": main()
