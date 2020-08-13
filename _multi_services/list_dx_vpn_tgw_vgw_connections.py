"""
Output: Look up some network details (DX connections, VIF, VPN connections, Transit gateway attachments)
"""
import click
import json
import logging
from os import makedirs
from os.path import join
from arki_common.aws import AwsApiHelper, get_tag_value

logging.getLogger().setLevel(logging.DEBUG)

DATA_ROOT = "data"
makedirs(DATA_ROOT, exist_ok=True)


def write_json_file(entity, data, account_id, region):
    if data:
        filename = join(DATA_ROOT, f"{entity}-{account_id}-{region}.json")
        with open(filename, "w") as outfile:
            json.dump(data, outfile, indent=2)


class Helper(AwsApiHelper):

    def get_dx_connections(self, session, account_id, region):
        client = session.client("directconnect", region_name=region)
        data = client.describe_connections()["connections"]
        write_json_file("dx_connections", data, account_id, region)
        return data

    def get_vifs(self, session, account_id, region):
        client = session.client("directconnect", region_name=region)
        data = client.describe_virtual_interfaces()["virtualInterfaces"]
        write_json_file("vifs", data, account_id, region)
        return data

    def get_vgws(self, session, account_id, region):
        client = session.client("directconnect", region_name=region)
        data = client.describe_virtual_gateways()["virtualGateways"]
        write_json_file("vgws", data, account_id, region)
        return data

    def get_vpn_connections(self, session, account_id, region):
        client = session.client("ec2", region_name=region)
        data = []

        for item in client.describe_vpn_connections()["VpnConnections"]:
            tunnels = {}
            for tunnel in item["Options"]["TunnelOptions"]:
                tunnels[tunnel["OutsideIpAddress"]] = {
                    "TunnelInsideCidr": tunnel["TunnelInsideCidr"],
                }
            for tele in item["VgwTelemetry"]:
                tunnels[tele["OutsideIpAddress"]].update({
                    "Status": tele["Status"],
                    "StatusMessage": tele["StatusMessage"],
                    "AcceptedRouteCount": tele["AcceptedRouteCount"],
                })

            cnt = 1
            for outside_ip, values in tunnels.items():
                data.append({
                    "VpnConnectionId": item["VpnConnectionId"],
                    "AccountId": account_id,
                    "CustomerGatewayId": item["CustomerGatewayId"],
                    "TransitGatewayId": item["TransitGatewayId"],
                    "OutsideIpAddress": outside_ip,
                    "Name": f'{get_tag_value(item["Tags"], "Name")}-{cnt}',
                    **values
                })
                cnt += 1
        write_json_file("vpn_connections", data, account_id, region)
        return data

    def get_tgws(self, session, account_id, region):
        client = session.client("ec2", region_name=region)
        data = []
        for page in client.get_paginator("describe_transit_gateways").paginate().result_key_iters():
            for item in page:
                data.append({
                    "TransitGatewayId": item["TransitGatewayId"],
                    "State": item["State"],
                    "OwnerId": item["OwnerId"],
                    "Description": item["Description"],
                    "Name": get_tag_value(item["Tags"], "Name"),
                })
        write_json_file("tgws", data, account_id, region)
        return data

    def get_tgw_attachments(self, session, account_id, region):
        client = session.client("ec2", region_name=region)
        data = []
        for page in client.get_paginator("describe_transit_gateway_attachments").paginate().result_key_iters():
            for item in page:
                data.append({
                    "TransitGatewayAttachmentId": item["TransitGatewayAttachmentId"],
                    "TransitGatewayId": item["TransitGatewayId"],
                    "TransitGatewayOwnerId": item["TransitGatewayOwnerId"],
                    "ResourceOwnerId": item["ResourceOwnerId"],
                    "ResourceType": item["ResourceType"],
                    "State": item["State"],
                    "Name": get_tag_value(item["Tags"], "Name"),
                })
        write_json_file("tgw_attachments", data, account_id, region)
        return data

    def get_tgw_vpc_attachments(self, session, account_id, region):
        client = session.client("ec2", region_name=region)
        data = []
        for page in client.get_paginator("describe_transit_gateway_vpc_attachments").paginate().result_key_iters():
            for item in page:
                data.append({
                    "TransitGatewayAttachmentId": item["TransitGatewayAttachmentId"],
                    "TransitGatewayId": item["TransitGatewayId"],
                    "VpcId": item["VpcId"],
                    "VpcOwnerId": item["VpcOwnerId"],
                    "SubnetIds": item["SubnetIds"],
                    "State": item["State"],
                    "Name": get_tag_value(item["Tags"], "Name"),
                })
        write_json_file("tgw_vpc_attachments", data, account_id, region)
        return data

    def process_request(self, session, account_id, region, kwargs):
        self.get_dx_connections(session, account_id, region)
        self.get_vifs(session, account_id, region)
        self.get_vgws(session, account_id, region)
        self.get_vpn_connections(session, account_id, region)
        self.get_tgws(session, account_id, region)
        self.get_tgw_attachments(session, account_id, region)
        self.get_tgw_vpc_attachments(session, account_id, region)


@click.command()
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(profile, region):
    Helper().start(profile, region, "ec2")


if __name__ == "__main__":
    main()
