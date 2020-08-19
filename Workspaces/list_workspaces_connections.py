from boto3.session import Session
import click
import os
import json


SUBNET_FIELDS = [
    "AvailabilityZone",
    "AvailabilityZoneId",
    "CidrBlock",
    "DefaultForAz",
    "VpcId",
    "State",
]
subnets = {}


def get_subnet(subnet_id, ec2_client):
    if subnet_id is None:
        return {}
    if subnet_id not in subnets:
        item = ec2_client.describe_subnets(SubnetIds=[subnet_id])["Subnets"][0]
        data = {f"Subnet{k}": item[k] for k in SUBNET_FIELDS}
        data["SubnetName"] = get_tag_value(item["Tags"])
        subnets[subnet_id] = data
    return subnets[subnet_id]


def get_tag_value(tags, key="Name"):
    for tag in tags:
        if tag["Key"] == key:
            return tag["Value"]
    return ""


def write_json_file(output_file, data):
    with open(output_file, "w") as outfile:
        json.dump(data, outfile, indent=2, sort_keys=True, default=str)


def process_account(session, region, detailed):
    results = []

    account_id = session.client("sts").get_caller_identity()["Account"]
    regions = session.get_available_regions("workspaces") \
        if region is None or region.lower() == "all" else [region]

    for region in regions:
        print(f"Checking {account_id} {region}...")

        client = session.client("workspaces", region_name=region)
        ec2_client = session.client("ec2", region_name=region)
        cnt = 0

        for response in client.get_paginator("describe_workspaces").paginate():
            for w in response["Workspaces"]:
                print(f"Checking {cnt} {w['WorkspaceId']}")
                lastlogon = client.describe_workspaces_connection_status(WorkspaceIds=[w["WorkspaceId"]])

                if detailed:
                    if w.get("SubnetId") is None:
                        print(w)
                    subnet = get_subnet(w.get("SubnetId"), ec2_client)
                    w.update({
                        "Account": account_id,
                        "Region": region,
                        "WorkspacesConnectionStatus": lastlogon["WorkspacesConnectionStatus"],
                        "TagList": client.describe_tags(ResourceId=w["WorkspaceId"])["TagList"],
                        **subnet,
                    })
                    #print(json.dumps(w, indent=2, sort_keys=True, default=str))
                    results.append(w)

                else:
                    data = [
                        w["WorkspaceId"],
                        w["UserName"],
                        w["WorkspaceId"],
                        lastlogon["WorkspacesConnectionStatus"][0]["ConnectionStateCheckTimestamp"]
                          if lastlogon["WorkspacesConnectionStatus"] else None,
                    ]
                    print(data)
                cnt += 1
        print(f"Total: {cnt}")

    return results


@click.command()
@click.option("--detailed", "-d", show_default=True, is_flag=True)
@click.option("--profile", "-p", help="AWS profile name", default="default")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(detailed, profile, region):
    session = Session(profile_name=profile)

    results = process_account(session, region, detailed)
    if results:
        write_json_file("workspaces.json", results)
        print(f"Total: {len(results)}")


if __name__ == "__main__":
    main()
