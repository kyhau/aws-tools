"""
(1) Print details of the attack(s) of the given attack ID or resource ARN, or
(2) Check if the top 5 contributor IPs of a shield attack are in give IP ranges.
"""
import json
from ipaddress import ip_address, ip_network

import boto3
import click
import requests

SRC_FILE = None  # If specified, a http url of a file containing cidr per line

is_in_range = lambda ip, cidr: ip_address(ip) in ip_network(cidr)


def get_known_ips(src_file):
    return [] if src_file is None else list(map(str.strip, requests.get(src_file).text.split("\n")))


def find_ip_in_known_ips(ip, cidrs):
    for cidr in cidrs:
        if is_in_range(ip, cidr):
            return True
    return False


def find_attacks(attack_id, resource_arn, cidrs):
    client = boto3.client("shield")

    attack_id_list = []
    if attack_id:
        attack_id_list = [attack_id]
    elif resource_arn:
        print(f"Get AttackIds for ResourceArn={resource_arn}")
        for page in client.get_paginator("list_attacks").paginate(ResourceArns=[resource_arn]).result_key_iters():
            for item in page:
                attack_id_list.append(item["AttackId"])
    else:
        raise Exception("Neither attach-id nor resource-arn provided")

    for attack_id in attack_id_list:
        print(f"Check AttackId={attack_id} for ResourceArn={resource_arn}")

        attack = client.describe_attack(AttackId=attack_id)["Attack"]

        if cidrs:
            for attack_property in attack["AttackProperties"]:
                if attack_property["AttackPropertyIdentifier"] == "SOURCE_IP_ADDRESS":
                    for contributor in attack_property["TopContributors"]:
                        ip = contributor["Name"]
                        if find_ip_in_known_ips(ip, cidrs):
                            print(f"👍 IP {ip} found in known IP ranges")
                        else:
                            print(f"👎 IP {ip} not found in known IP ranges")
        else:
            print(json.dumps(attack, indent=2, default=str))


@click.command(help="Check if IP of an attack (of specific attack id or resource arn) is within known IP ranges")
@click.option("--attack-id", "-i", help="Attack ID")
@click.option("--resource-arn", "-r", help="Resource ARN")
def main(attack_id, resource_arn):
    cidrs = get_known_ips(SRC_FILE)

    if attack_id or resource_arn:
        find_attacks(attack_id, resource_arn, cidrs)
    else:
        for cidr in sorted(cidrs):
            print(cidr)


if __name__ == "__main__":
     main()
