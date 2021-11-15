#!/usr/bin/env python
import json

import click
import requests

IP_TYPES = [
    "ipv4",
    "ipv6",
]

SERVICES = [
    "AMAZON",
    "AMAZON_APPFLOW",
    "AMAZON_CONNECT",
    "API_GATEWAY",
    "CHIME_MEETINGS",
    "CHIME_VOICECONNECTOR",
    "CLOUD9",
    "CLOUDFRONT",
    "CODEBUILD",
    "DYNAMODB",
    "EBS",
    "EC2",
    "EC2_INSTANCE_CONNECT",
    "GLOBALACCELERATOR",
    "KINESIS_VIDEO_STREAMS",
    "ROUTE53",
    "ROUTE53_HEALTHCHECKS",
    "ROUTE53_HEALTHCHECKS_PUBLISHING",
    "ROUTE53_RESOLVER",
    "S3",
    "WORKSPACES_GATEWAYS",
]

SOURCE = "https://ip-ranges.amazonaws.com/ip-ranges.json"


def list_ip_ranges(service, ip_type, region, prefix):
    data = requests.get().json(SOURCE)

    key_prefix, key_prefixes = ("ip_prefix", "prefixes") if ip_type == "ipv4" else ("ipv6_prefix", "ipv6_prefixes")

    prefixes = data[key_prefixes]

    ret = []
    for item in prefixes:
        if item["service"] != service:
            continue
        if region and region != item["region"]:
            continue
        if prefix and prefix != item[key_prefix] and not item[key_prefix].startswith(f"{prefix}/"):
            continue

        ret.append(item)

    print(json.dumps(ret, indent=2))
    print(f"CreateDate: {data['createDate']}")


@click.command(help="Get AWS public IP ranges")
@click.option("--prefix", "-p", help="Find the specified prefix e.g. 52.65.0.0/16 or 52.65.0.0; all if not specified")
@click.option("--region", "-r", help="AWS Region; not specified for all regions", default="ap-southeast-2")
@click.option("--service", "-s", required=True, type=click.Choice(SERVICES, case_sensitive=False))
@click.option("--ip-type", "-t", required=True, type=click.Choice(IP_TYPES, case_sensitive=False), default="ipv4", show_default=True)
def main(prefix, region, service, ip_type):
    list_ip_ranges(service.upper(), ip_type.lower(), region, prefix)


if __name__ == "__main__":
     main()
