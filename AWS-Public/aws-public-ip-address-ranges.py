#!/usr/bin/env python
import ipaddress
import json

import click
import requests
from InquirerPy import inquirer
from InquirerPy.base.control import Choice

IP_TYPES = {
    "ipv4": ("ip_prefix", "prefixes"),
    "ipv6": ("ipv6_prefix", "ipv6_prefixes")
}

SOURCE = "https://ip-ranges.amazonaws.com/ip-ranges.json"


def prompt_multi_selection(name, options, pre_selected_options, message=None):
    if not options:
        raise ValueError("No options retrieved for selection.")

    choices = [
        Choice(option, enabled=option in pre_selected_options)
        for option in options
    ]

    return inquirer.checkbox(
        message=message if message else f"Please choose the {name}",
        choices=choices,
        cycle=True,
        transformer=lambda result: f"{len(result)} {name} selected",
    ).execute()


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


def find_ip(ip, data, ip_type):
    key_prefix, key_prefixes = IP_TYPES[ip_type]
    target_ip = ipaddress.ip_address(ip)
    for item in data[key_prefixes]:
        if target_ip in ipaddress.ip_network(item[key_prefix]):
            print(f"Found {ip} in")
            print(json.dumps(item, indent=2))
            return True


@click.command(help="Get AWS public IP ranges, or check if a given IP is within AWS public IP ranges")
@click.option("--ip", "-i", help="IP address to search.")
@click.option("--prefix", "-p", help="Find the specified prefix e.g. 52.65.0.0/16 or 52.65.0.0; all if not specified")
@click.option("--region", "-r", help="AWS Region; not specified for all regions", default="ap-southeast-2")
@click.option("--ip-type", "-t", type=click.Choice(IP_TYPES, case_sensitive=False), default="ipv4", show_default=True)
@click.option("--services", "-s", multiple=True)
def main(ip, prefix, region, ip_type, services):
    data = requests.get(SOURCE).json()
    ip_type = ip_type.lower()

    if ip:
        find_ip(ip, data, ip_type)
        return

    if services:
        services = list(map(str.upper, services))
    else:
        services = select_services(data, ip_type)

    list_ip_ranges(data, services, ip_type.lower(), region, prefix)


if __name__ == "__main__":
     main()
