"""
List WorkSpaces details including
- Connection status
- Snapshots
- Subnets
"""
import json
import os
import time

import click
from boto3.session import Session

SUBNET_FIELDS = [
    "SubnetId",
    "SubnetName",
    "AvailabilityZone",
    "AvailabilityZoneId",
    "CidrBlock",
    "UsableIpAddressCount",
    "AvailableIpAddressCount",
    "DefaultForAz",
    "State",
    "VpcId",
]


def get_tag_value(tags, key="Name"):
    for tag in tags:
        if tag["Key"] == key:
            return tag["Value"]
    return ""


def write_csv_file(output_file, items):
    with open(output_file, "w") as f:
        f.write(f"{','.join(SUBNET_FIELDS)}\n")
        for item in items:
            f.write(f'{",".join(str(item[k]) for k in SUBNET_FIELDS)}\n')


def write_json_file(output_file, data):
    with open(output_file, "w") as outfile:
        json.dump(data, outfile, indent=2, sort_keys=True, default=str)


def get_subnets(session, regions):
    subnets = {}
    for region in regions:
        print(f"Checking {region}...")
        try:
            client = session.client("ec2", region_name=region)
            for page in client.get_paginator("describe_subnets").paginate().result_key_iters():
                for item in page:
                    mask = int(item["CidrBlock"].split("/")[1])
                    item["UsableIpAddressCount"] = 2**(32-mask) - 5  # 5 addresses reserved per subnet

                    item["SubnetName"] = get_tag_value(item["Tags"])

                    data = {k: item[k] for k in SUBNET_FIELDS}
                    subnets[item["SubnetId"]] = data
        except Exception as e:
            print(e)
    return subnets


def get_workspaces(session, regions, subnets, account_id, detailed):
    workspaces = []

    for region in regions:
        print(f"Checking {account_id} {region}...")
        client = session.client("workspaces", region_name=region)
        cnt = 0
        for response in client.get_paginator("describe_workspaces").paginate():
            for w in response["Workspaces"]:
                lastlogon = client.describe_workspaces_connection_status(WorkspaceIds=[w["WorkspaceId"]])

                if detailed:
                    print(f"Checking {cnt} {w['WorkspaceId']}")

                    subnet = subnets.get(w["SubnetId"], {})
                    snapshots = client.describe_workspace_snapshots(WorkspaceId=w["WorkspaceId"])
                    tags = client.describe_tags(ResourceId=w["WorkspaceId"])["TagList"]
                    w.update({
                        "Account": account_id,
                        "Region": region,
                        "RebuildSnapshot": snapshots["RebuildSnapshots"][0]["SnapshotTime"] if snapshots["RebuildSnapshots"] else None,
                        "RestoreSnapshot": snapshots["RestoreSnapshots"][0]["SnapshotTime"] if snapshots["RestoreSnapshots"] else None,
                        "WorkspacesConnectionStatus": lastlogon["WorkspacesConnectionStatus"],
                        "TagList": tags,
                        **subnet,
                    })
                    #print(json.dumps(w, indent=2, sort_keys=True, default=str))
                    workspaces.append(w)
                    time.sleep(0.5)

                else:
                    data = [
                        w["WorkspaceId"],
                        w["UserName"],
                        w["WorkspaceId"],
                        str(lastlogon["WorkspacesConnectionStatus"][0]["ConnectionStateCheckTimestamp"])
                          if lastlogon["WorkspacesConnectionStatus"] else None,
                    ]
                    print(data)
                cnt += 1

        print(f"Total: {cnt}")

    return workspaces


@click.command()
@click.option("--detailed", "-d", show_default=True, is_flag=True)
@click.option("--profile", "-p", help="AWS profile name", default="default")
@click.option("--region", "-r", help="AWS Region. All regions if not specified")
def main(detailed, profile, region):
    session = Session(profile_name=profile)

    account_id = session.client("sts").get_caller_identity()["Account"]

    subnets = {}
    if detailed:
        regions = session.get_available_regions("ec2") if region is None else [region]
        subnets = get_subnets(session, regions)
        if subnets:
            write_csv_file("subnets.csv", list(subnets.values()))

    regions = session.get_available_regions("workspaces") if region is None else [region]
    workspaces = get_workspaces(session, regions, subnets, account_id, detailed)
    if workspaces:
        write_json_file("workspaces.json", workspaces)
        print(f"Total: {len(workspaces)}")


if __name__ == "__main__":
    main()
