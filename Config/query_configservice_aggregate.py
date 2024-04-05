"""
Using select_aggregate_resource_config to query resources through Aggregator.

You can optionally provide path to sql files through argument, if not, you will be prompted
to select from a list of predefined SQL files from the default directory.
"""
import glob
import logging
from os.path import basename, dirname, exists, join
from shutil import rmtree

import click
from boto3.session import Session
from helper.selector import prompt_single_selection

logging.getLogger().setLevel(logging.DEBUG)

DEFAULT_SQLFILE_ROOT = join(dirname(__file__).split(".")[0], "sql_files", "aggregate")


def select_sql_file(sql_files_dir=DEFAULT_SQLFILE_ROOT):
    files = glob.glob(f"{sql_files_dir}/*")
    return prompt_single_selection("SqlFile", options=files)


def process_request(aggregator, sql_file, profile, region):
    sql_statement = None
    with open(sql_file, "r") as f:
        sql_statement = f.read()

    output_filename = f'{basename(sql_file).replace(".sql", "")}.txt'
    if exists(output_filename):
        rmtree(output_filename)

    session = Session(profile_name=profile)
    client = session.client("config", region_name=region)
    params = {
        "Expression": sql_statement,
        "ConfigurationAggregatorName": aggregator,
    }
    while True:
        resp = client.select_aggregate_resource_config(**params)
        for item in resp["Results"]:
            dump(item, output_filename)

        if resp.get("NextToken") is None:
            break
        params["NextToken"] = resp.get("NextToken")


def dump(data, output_filename, to_console=True):
    if to_console is True:
        print(data)
    with open(output_filename, "a") as f:
        f.write(f'{data}\n')


@click.command()
@click.option("--aggregator", "-a", required=True, help="Name of the configuration aggregator")
@click.option("--sqlfilesdir", "-d", default=DEFAULT_SQLFILE_ROOT, help="Directory of the SQL files")
@click.option("--profile", "-p", default="default", show_default=True, help="AWS profile name")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region")
def main(aggregator, sqlfilesdir, profile, region):
    sql_file = select_sql_file(sqlfilesdir)
    process_request(aggregator, sql_file, profile, region)


if __name__ == "__main__":
    main()
