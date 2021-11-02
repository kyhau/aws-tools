"""
Identify databases hosted in EC2 instances, by inspecting security groups for common database ports.
"""
import click
import logging
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)

common_db_server_ports = [
    1433,   # MS SQL Server
    3306,   # MySQL
    5432,   # PostgreSQL
    49000,  # Informix
]


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        client = session.client("ec2", region_name=region)
        for item in self.paginate(client, "describe_security_groups", kwargs):
            Helper.process_data(item, account_id, region, client)
            if kwargs.get("GroupIds"):
                return True

    @staticmethod
    def subnet_names(client, subnet_ids):
        ret = {}
        for subnet in client.describe_subnets(SubnetIds=subnet_ids)["Subnets"]:
            if "Tags" in subnet:
                name = None
                for tag in subnet["Tags"]:
                    if tag["Key"] == "Name":
                        name = tag["Value"]
                if name is not None:
                    ret[subnet["SubnetId"]] = name
        return ret
    
    @staticmethod
    def process_data(sg, account_id, region, client):
        ports_matched = {i.get("FromPort") for i in sg["IpPermissions"] if i.get("FromPort") in common_db_server_ports}
        if not ports_matched:
            return

        ret = client.describe_network_interfaces(Filters=[{"Name": "group-id", "Values": [sg["GroupId"]]}])

        instance_id_subnet_set = {
            (r["Attachment"]["InstanceId"], r["SubnetId"])
            for r in ret["NetworkInterfaces"]
            if "Attachment" in r and "InstanceId" in r["Attachment"]
        }

        if instance_id_subnet_set:
            subnet_ids = {y for (x, y) in instance_id_subnet_set}
            subnet_id_dict_data = Helper.subnet_names(client, list(subnet_ids))
            for (instance_id, subnet_id) in instance_id_subnet_set:
                data = [
                    account_id,
                    region,
                    sg["GroupId"],
                    "|".join(map(str, ports_matched)),
                    instance_id,
                    subnet_id_dict_data[subnet_id],  # subnet name
                ]
                print(",".join(data))


@click.command()
@click.option("--groupid", "-i", help="Security Group ID.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(groupid, profile, region):
    kwargs = {"GroupIds": [groupid]} if groupid else {}
    Helper().start(profile, region, "ec2", kwargs)


if __name__ == "__main__":
    main()
