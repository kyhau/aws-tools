from boto3.session import Session
from botocore.exceptions import ClientError
import click
from configparser import ConfigParser
import logging
from os.path import basename, exists, expanduser, join
from shutil import rmtree

logging.getLogger().setLevel(logging.DEBUG)

aws_profiles = []
try:
    cp = ConfigParser()
    cp.read(join(expanduser("~"), ".aws", "credentials"))
    aws_profiles = cp.sections()
except Exception as e:
    logging.error(e)


def dump(data, output_filename, to_console=True):
    if to_console is True:
        print(data)
    with open(output_filename, "a") as f:
        f.write(f'{data}\n')


def list_action(session, sql_statement, sqlfile):
    account_id = session.client("sts").get_caller_identity()["Account"]
    
    output_filename = f'{account_id}_{basename(sqlfile).replace(".sql", "")}.txt'
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
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--sqlfile", "-s", required=True, help="File containing the sql statement (.sql)")
def main(profile, sqlfile):
    with open(sqlfile, "r") as f:
        sql_statement = f.read()

    profile_names = [profile] if profile else aws_profiles

    for profile_name in profile_names:
        session = Session(profile_name=profile_name)
        list_action(session, sql_statement, sqlfile)


if __name__ == "__main__": main()
