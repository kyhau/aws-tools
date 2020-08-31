"""
A simple script to restore/rebuild a WorkSpace and wait for the state to become AVAILABLE.
"""
import json
import os
import time
from datetime import datetime

import click
from boto3.session import Session


def wait_for_status(client, workspace_id):
    state = client.describe_workspaces(WorkspaceIds=[workspace_id])["Workspaces"][0]["State"]

    # 'State': 'PENDING'|'AVAILABLE'|'IMPAIRED'|'UNHEALTHY'|'REBOOTING'|'STARTING'
    # |'REBUILDING'|'RESTORING'|'MAINTENANCE'|'ADMIN_MAINTENANCE'|'TERMINATING'
    # |'TERMINATED'|'SUSPENDED'|'UPDATING'|'STOPPING'|'STOPPED'|'ERROR'
    while state.endswith("ING"):
        print(state)
        time.sleep(30)
        state = client.describe_workspaces(WorkspaceIds=[workspace_id])["Workspaces"][0]["State"]


def restore_workspace(client, workspace_id):
    resp = client.restore_workspace(WorkspaceId=workspace_id)
    print(resp)
    # resp is always {}, exception raised if error


def rebuild_workspace(client, workspace_id):
    resp = client.rebuild_workspaces(
        RebuildWorkspaceRequests=[
            {
                "WorkspaceId": workspace_id,
            },
        ]
    )
    print(resp)


@click.command()
@click.option('--op', type=click.Choice(['restore', 'rebuild', 'wait'], case_sensitive=False))
@click.option("--workspaceid", "-w", help="WorkSpace ID")
@click.option("--profile", "-p", help="AWS profile name", default="default")
def main(op, workspaceid, profile):
    start_time = datetime.now()
    print(f"Started time: {start_time}")

    try:
        client = Session(profile_name=profile).client("workspaces")

        if op == "restore":
            restore_workspace(client, workspaceid)
            time.sleep(10)

        elif op == "rebuild":
            rebuild_workspace(client, workspaceid)
            time.sleep(10)
            # Status: REBUILDING -> PENDING -> AVAILABLE

        wait_for_status(client, workspaceid)

    except Exception as e:
        print(e)
    finally:
        end_time = datetime.now()
        print(f"Ended time: {end_time}")
        print(f"Total time: {end_time - start_time}")


if __name__ == "__main__":
   main()
