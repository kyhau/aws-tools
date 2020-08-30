"""
A helper script to call describe_vpc_endpoint_services.
"""
import click
import logging
import yaml
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def __init__(self, endpoint_type, name_only):
        super().__init__()
        self._endpoint_type = endpoint_type
        self._name_only = name_only

    def process_request(self, session, account_id, region, kwargs):
        cnt = 0
        client = session.client("ec2", region_name=region)
        for item in self.paginate(client, "describe_vpc_endpoint_services", kwargs):
            if self.match_service_type(item):
                if self._name_only:
                    if "ServiceName" in item:
                        print(item["ServiceName"])
                    else:
                        print(item)
                else:
                    print(yaml.dump(item))
                    print("--------------------------------------------------------------------------------")
                cnt += 1
        logging.debug(f"{account_id} {region}: Total items: {cnt}")

    def match_service_type(self, item):
        if self._endpoint_type is None:
            return True
    
        for subitem in item["ServiceType"]:
            curr = subitem.get("ServiceType")
            if curr is not None and curr.lower() == self._endpoint_type:
                return True
        return False


@click.command()
@click.option("--endpointtype", "-t", help="VPC endpoint type (Gateway|Interface). Return all if not specified.")
@click.option("--nameonly", "-n", is_flag=True, show_default=True, help="Show names only")
@click.option("--servicename", "-s", help="Service name. Optional. E.g. com.amazonaws.ap-southeast-2.s3")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(endpointtype, nameonly, servicename, profile, region):
    kwargs = {"ServiceNames": [servicename]} if servicename else {}
    Helper(endpointtype, nameonly).start(profile, region, "ec2", kwargs)


if __name__ == "__main__":
    main()
