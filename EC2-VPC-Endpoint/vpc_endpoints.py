"""
A helper script to call describe_vpc_endpoints as well as lookup ENI IPs.
"""
from boto3.session import Session
from botocore.exceptions import ClientError
import click
import logging
from time import time
import yaml
from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def __init__(self, endpoint_type):
        super().__init__()
        self._endpoint_type = endpoint_type

    def process_request(self, session, account_id, region, kwargs):
        cnt = 0
        client = session.client("ec2", region_name=region)
        for item in self.paginate(client, "describe_vpc_endpoints", kwargs):
            if self._endpoint_type and self._endpoint_type != item["VpcEndpointType"].lower():
                continue
        
            if item["NetworkInterfaceIds"]:
                # Retrieve also the primary private IPs for the ENIs
                resp2 = client.describe_network_interfaces(NetworkInterfaceIds=item["NetworkInterfaceIds"])
                eni_data = [
                    f'{item2["NetworkInterfaceId"]}, {item2["PrivateIpAddress"]}' for item2 in
                    resp2["NetworkInterfaces"]
                ]
                item["NetworkInterfaceIds"] = eni_data
        
            print(yaml.dump(item))
            print("--------------------------------------------------------------------------------")
            cnt += 1
        logging.debug(f"Total items: {cnt}")


def new_operation_params(endpoint_id, service_name, vpc_id):
    operation_params = {"Filters": []}
    if endpoint_id:
        operation_params["VpcEndpointIds"] = [endpoint_id]
    if service_name:
        operation_params["Filters"].append({"Name": "service-name", "Values": [service_name]})
    if vpc_id:
        operation_params["Filters"].append({"Name": "vpc-id", "Values": [vpc_id]})
    return operation_params


@click.command()
@click.option("--endpointid", "-e", help="VPC endpoint ID. Optional. E.g. vpce-123456789012")
@click.option("--endpointtype", "-t", help="VPC endpoint type (Gateway|Interface). Return all if not specified.")
@click.option("--servicename", "-s", help="Service name. Optional. E.g. com.amazonaws.ap-southeast-2.s3")
@click.option("--vpcid", "-v", help="VPC ID. Optional. E.g. vpc-123456789012")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(endpointid, endpointtype, servicename, vpcid, profile, region):
    kwargs = new_operation_params(endpointid, servicename, vpcid)
    endpointtype = endpointtype if endpointtype is None else endpointtype.lower()
    Helper(endpointtype).start(profile, region, "ec2", kwargs)


if __name__ == "__main__":
    main()
