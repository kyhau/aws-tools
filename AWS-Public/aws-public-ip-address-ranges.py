#!/usr/bin/env python
import json

import click
import requests
from helper.selector import prompt_multi_selection

IP_TYPES = {
    "ipv4": ("ip_prefix", "prefixes"),
    "ipv6": ("ipv6_prefix", "ipv6_prefixes")
}

SOURCE = "https://ip-ranges.amazonaws.com/ip-ranges.json"


def list_ip_ranges(data, services, ip_type, region, prefix):
    key_prefix, key_prefixes = IP_TYPES[ip_type]

    ret = []
    for item in data[key_prefixes]:
        if item["service"] not in services:
            continue
        if region and region != item["region"]:
            continue
        if prefix and prefix != item[key_prefix] and not item[key_prefix].startswith(f"{prefix}/"):
            continue

        ret.append(item)

    print(json.dumps(ret, indent=2))


def select_services(data, ip_type):
    _, key_prefixes = IP_TYPES[ip_type]
    services = sorted(set( d["service"] for d in data[key_prefixes]))
    return prompt_multi_selection("Service", options=services, pre_selected_options=[])


@click.command(help="Get AWS public IP ranges")
@click.option("--prefix", "-p", help="Find the specified prefix e.g. 52.65.0.0/16 or 52.65.0.0; all if not specified")
@click.option("--region", "-r", help="AWS Region; not specified for all regions", default="ap-southeast-2")
@click.option("--ip-type", "-t", type=click.Choice(IP_TYPES, case_sensitive=False), default="ipv4", show_default=True)
@click.option("--services", "-s", multiple=True)
def main(prefix, region, ip_type, services):
    data = requests.get(SOURCE).json()
    ip_type = ip_type.lower()

    if services:
        services = list(map(str.upper, services))
    else:
        services = select_services(data, ip_type)

    list_ip_ranges(data, services, ip_type.lower(), region, prefix)


if __name__ == "__main__":
     main()
