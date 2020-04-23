from boto3.session import Session
import click


def process(client):
    paginator = client.get_paginator("describe_workspaces")
    for response in paginator.paginate():
        for i in response["Workspaces"]:
            lastlogon = client.describe_workspaces_connection_status(
                WorkspaceIds=[
                    i["WorkspaceId"]
                ]
            )
            print(
                i["WorkspaceId"],
                i["UserName"],
                i["WorkspaceId"],
                lastlogon["WorkspacesConnectionStatus"][0]["ConnectionStateCheckTimestamp"]
            )


################################################################################
# Entry point

@click.command()
@click.option("--profile", "-p", help="AWS profile name", default="default")
@click.option("--region", "-r", help="AWS Region; default ap-southeast-2", default="ap-southeast-2")
def main(profile, region):
    session = Session(profile_name=profile)
    client = session.client("workspaces", region_name=region)
    process(client)


if __name__ == "__main__": main()
