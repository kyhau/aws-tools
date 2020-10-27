"""
List WorkSpaces details including
- Connection status
- Snapshots
- Subnets
"""
import json
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


def get_workspace(client, w, account_id, region, subnets, cnt, detailed):
    attempts = 1
    while attempts <= 3:
        try:
            workspace_id = w["WorkspaceId"]
            lastlogon = client.describe_workspaces_connection_status(WorkspaceIds=[workspace_id])

            if detailed:
                print(f"Checking {cnt} {workspace_id} (attempt {attempts})")
                # No SubnetId means the subnet in which the WorkSpace was launched does not have an available private IP address
                subnet = subnets.get(w.get("SubnetId"), {})
                snapshots = client.describe_workspace_snapshots(WorkspaceId=workspace_id)
                tags = client.describe_tags(ResourceId=workspace_id)["TagList"]
                data = w
                data.update({
                    "Account": account_id,
                    "Region": region,
                    "RebuildSnapshot": snapshots["RebuildSnapshots"][0]["SnapshotTime"] if snapshots["RebuildSnapshots"] else None,
                    "RestoreSnapshot": snapshots["RestoreSnapshots"][0]["SnapshotTime"] if snapshots["RestoreSnapshots"] else None,
                    "WorkspacesConnectionStatus": lastlogon["WorkspacesConnectionStatus"],
                    "TagList": tags,
                    **subnet,
                })
                #print(json.dumps(data, indent=2, sort_keys=True, default=str))

            else:
                data = [
                    workspace_id,
                    w["UserName"],
                    workspace_id,
                    str(lastlogon["WorkspacesConnectionStatus"][0]["ConnectionStateCheckTimestamp"])
                        if lastlogon["WorkspacesConnectionStatus"] else None,
                ]
                print(data)
            return data
        except Exception as e:  # ThrottlingException
            print(e)
            time.sleep(5)
        attempts += 1
    print(f'Giving up on {w["WorkspaceId"]}')
    return w


def get_workspaces(session, regions, subnets, account_id, detailed, workspace_id):
    workspaces = []

    params = {} if workspace_id is None else {"WorkspaceIds": [workspace_id]}

    for region in regions:
        print(f"Checking {account_id} {region}...")

        client = session.client("workspaces", region_name=region)
        cnt = 0

        for response in client.get_paginator("describe_workspaces").paginate(**params):
            for w in response["Workspaces"]:
                w2 = get_workspace(client, w, account_id, region, subnets, cnt, detailed)
                workspaces.append(w2)
                cnt += 1

            if workspace_id:
                return workspaces

        print(f"Total: {cnt}")

    return workspaces


@click.command()
@click.option("--detailed", "-d", show_default=True, is_flag=True)
@click.option("--workspaceid", "-w", help="WorkSpace ID")
@click.option("--profile", "-p", help="AWS profile name", default="default")
@click.option("--region", "-r", help="AWS Region. All regions if not specified")
def main(detailed, workspaceid, profile, region):
    session = Session(profile_name=profile)

    account_id = session.client("sts").get_caller_identity()["Account"]

    subnets = {}
    if detailed:
        regions = session.get_available_regions("ec2") if region is None else [region]
        subnets = get_subnets(session, regions)
        if subnets:
            write_csv_file("subnets.csv", list(subnets.values()))

    regions = session.get_available_regions("workspaces") if region is None else [region]
    workspaces = get_workspaces(session, regions, subnets, account_id, detailed, workspaceid)
    if workspaces:
        if workspaceid:
            print(json.dumps(workspaces, indent=2, sort_keys=True, default=str))
        else:
            write_json_file("workspaces.json", workspaces)
            print(f"Total: {len(workspaces)}")


if __name__ == "__main__":
    main()
