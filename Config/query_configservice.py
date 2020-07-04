import click
import logging
from os.path import basename, exists
from shutil import rmtree
from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def __init__(self, sql_file):
        super().__init__()
        self._sql_file = sql_file
        with open(sql_file, "r") as f:
            self._sql_statement = f.read()

    def process_request(self, session, account_id, region, kwargs):
        output_filename = f'{account_id}_{region}_{basename(self._sql_file).replace(".sql", "")}.txt'
        if exists(output_filename):
            rmtree(output_filename)

        client = session.client("config", region_name=region)
        resp = client.select_resource_config(Expression=self._sql_statement)
        next_token = resp.get("NextToken")
        for item in resp["Results"]:
            dump(item, output_filename)
    
        while next_token:
            resp = client.select_resource_config(Expression=self._sql_statement, NextToken=next_token)
            next_token = resp.get("NextToken")
            for item in resp["Results"]:
                dump(item, output_filename)


def dump(data, output_filename, to_console=True):
    if to_console is True:
        print(data)
    with open(output_filename, "a") as f:
        f.write(f'{data}\n')


@click.command()
@click.option("--sqlfile", "-s", required=True, help="File containing the sql statement (.sql)")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(sqlfile, profile, region):
    Helper(sqlfile).start(profile, region, "config")


if __name__ == "__main__":
    main()
