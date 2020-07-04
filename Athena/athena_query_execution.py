"""
A Athena helper script for executing SQL statement in SQL file(s).
"""
from boto3.session import Session
import click
import logging
from os.path import join
from os import walk
import time

logging.getLogger().setLevel(logging.INFO)


def read_sql_file(filename):
    with open(filename, "r") as sql_file:
        content = sql_file.read()
    return content.replace("\n", " ").replace(";", "")


def get_sql_files(root_dir):
    sql_files = []
    for root, _, files in walk(root_dir):
        sql_files.extend(join(root, file) for file in files if file.endswith(".sql"))
    return sql_files


def athena_to_s3(session, region, database, output, workgroup, sql_file, max_execution_time):
    client = session.client("athena", region_name=region)
    
    params = {}
    if output:
        params.update({"ResultConfiguration": {"OutputLocation": output}})
    if workgroup:
        params.update({"WorkGroup": workgroup})
    
    execution = client.start_query_execution(
        QueryString=read_sql_file(sql_file),
        QueryExecutionContext={"Database": database},
        **params
    )
    execution_id = execution["QueryExecutionId"]
    state = "RUNNING"

    while max_execution_time > 0 and state in ["QUEUED", "RUNNING"]:
        max_execution_time -= 1
        response = client.get_query_execution(QueryExecutionId=execution_id)
        state = response.get("QueryExecution", {}).get("Status", {}).get("State")

        # 'QUEUED'|'RUNNING'|'SUCCEEDED'|'FAILED'|'CANCELLED'
        logging.info(f"Current state: {state}")
        if state in ["QUEUED", "RUNNING"]:
            time.sleep(1)

        elif state == "SUCCEEDED":
            print(f'Output Location: {response.get("QueryExecution", {}).get("ResultConfiguration", {}).get("OutputLocation")}')
            print("Results:")
            for page in client.get_paginator("get_query_results").paginate(QueryExecutionId=execution_id).result_key_iters():
                for item in page:
                    print(", ".join([x["VarCharValue"] for x in item["Data"]]))

        elif state in ["FAILED", "CANCELLED"]:
            logging.error(response["QueryExecution"]["Status"]["StateChangeReason"])


@click.group(help="A Athena helper script for executing SQL.")
@click.option("--database", "-d", default="default", show_default=True, help="Athena database name")
@click.option("--workgroup", "-w", default="primary", show_default=True, help="Athena Workgroup name")
@click.option("--output", "-o", help="S3 output location: e.g. s3://path/to/query/bucket/")
@click.option("--max-execution-time", "-m", default=60, show_default=True, help="Max execution time in second")
@click.option("--profile", "-p", default="default", show_default=True, help="AWS profile name")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region")
@click.pass_context
def main_cli(ctx, database, workgroup, output, max_execution_time, profile, region):
    ctx.obj = {
        "database": database,
        "output": output,
        "workgroup": workgroup,
        "max_execution_time": max_execution_time,
        "region": region,
        "session": Session(profile_name=profile),
    }


@main_cli.command(help="Execute all .sql files in the given path.")
@click.argument("path", required=True)
@click.pass_context
def sql_dir(ctx, path):
    for sql_file in get_sql_files(path):
        athena_to_s3(sql_file=sql_file, **ctx.obj)


@main_cli.command(help="Execute SQL statement in the given .sql file.")
@click.argument("file", required=True)
@click.pass_context
def sql_file(ctx, file):
    athena_to_s3(sql_file=file, **ctx.obj)


if __name__ == "__main__":
    main_cli(obj={})
