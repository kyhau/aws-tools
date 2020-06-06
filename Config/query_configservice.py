from boto3.session import Session
from botocore.exceptions import ClientError
import click
import logging
from os.path import basename, exists
from shutil import rmtree
from time import time

# Update the root logger to get messages at DEBUG and above
logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)


def read_aws_profile_names():
    from configparser import ConfigParser
    from os.path import expanduser, join
    try:
        cp = ConfigParser()
        cp.read(join(expanduser("~"), ".aws", "credentials"))
        return cp.sections()
    except Exception as e:
        logging.error(e)


def dump(data, output_filename, to_console=True):
    if to_console is True:
        print(data)
    with open(output_filename, "a") as f:
        f.write(f'{data}\n')


def list_action(session, sql_statement, sqlfile, aws_region):
    account_id = session.client("sts").get_caller_identity()["Account"]
    
    output_filename = f'{account_id}_{basename(sqlfile).replace(".sql", "")}.txt'
    if exists(output_filename):
        rmtree(output_filename)

    regions = session.get_available_regions("config") if aws_region == "all" else [aws_region]
    for region in regions:
        try:
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
            error_code = e.response["Error"]["Code"]
            if error_code in ["UnrecognizedClientException"]:
                logging.warning(f"Unable to process region {region}: {error_code}")
            else:
                raise


@click.command()
@click.option("--sqlfile", "-s", required=True, help="File containing the sql statement (.sql)")
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--region", "-r", help="AWS Region; use 'all' for all regions.", default="ap-southeast-2")
def main(sqlfile, profile, region):
    start = time()
    try:
        with open(sqlfile, "r") as f:
            sql_statement = f.read()
    
        profile_names = [profile] if profile else read_aws_profile_names()
    
        for profile_name in profile_names:
            session = Session(profile_name=profile_name)
            list_action(session, sql_statement, sqlfile, region)
    finally:
        logging.info(f"Total execution time: {time() - start}s")


if __name__ == "__main__":
    main()
