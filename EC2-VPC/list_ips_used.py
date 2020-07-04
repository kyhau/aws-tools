"""
Given a profile or a list of role arns, retrieve all IPs currently used in the corresponding account and write them to
a csv file (<account_id>_ips_used.csv).

Output data:
PrivateIpAddress, PrivateDnsName, IsPrimary, PublicIp, PublicDnsName, InstanceId, Description, AccountId, Region

`Description` is the instance's tag `Name` if the IP is used by an instance; otherwise it is the ENI description.
"""
from botocore.exceptions import ClientError
import click
import logging
from arki_common.aws import AwsApiHelper, get_tag_value
from arki_common.file_io import write_csv_file

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def process_account(self, session, account_id, aws_region, service, kwargs):
        results = []
        for region in session.get_available_regions(service) if aws_region == "all" else [aws_region]:
            try:
                logging.debug(f"Checking {account_id} {region}")
                
                client = session.client("ec2", region_name=region)
                for ni in self.paginate(client, "describe_network_interfaces"):
                    if ni["Status"] != "in-use":
                        continue
                    
                    d1 = ni["Attachment"].get("InstanceId") if "Attachment" in ni else None
                    instance = client.describe_instances(InstanceIds=[d1])["Reservations"][0]["Instances"][0]
                    d2 = ni["Description"] if d1 is None else get_tag_value(instance.get("Tags",[]))
                    
                    for data in ni["PrivateIpAddresses"]:
                        results.append([
                            data["PrivateIpAddress"],
                            data["PrivateDnsName"],
                            data["Primary"],
                            data["Association"].get("PublicIp") if "Association" in data else None,
                            data["Association"].get("PublicDnsName") if "Association" in data else None,
                            d1, d2, account_id, region
                        ])
            except ClientError as e:
                self.process_client_error(e, account_id, region)
        
        if results:
            output_filename = f"{account_id}_ips_used.csv"
            titles = [
                "PrivateIpAddress", "PrivateDnsName", "IsPrimary", "PublicIp", "PublicDnsName", "InstanceId", "Description",
                "AccountId", "Region"]
            results.insert(0, titles)
            write_csv_file(results, output_filename)


@click.command()
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(profile, region):
    Helper().start(profile, region, "ec2")


if __name__ == "__main__":
    main()
