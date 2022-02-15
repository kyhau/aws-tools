import click
import logging
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)

app_names = [
    "Microsoft SQL Server",  # MS SQL Server
    "sql",       # MMS SQL Server, MySQL Workbench, PostgreSQL
    "informix",  # IBM Informix
]


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        instance_id = kwargs["instance_id"]
        if instance_id:
            instance_ids = [instance_id]
        else:
            ec2 = session.resource("ec2", region_name=region)
            instance_ids = [instance.id for instance in ec2.instances.all()]
    
        for instance_id in instance_ids:
            client = session.client("ssm", region_name=region)
            resp = client.list_inventory_entries(InstanceId=instance_id, TypeName="AWS:Application")
            for entry in resp["Entries"]:
                matches = [d for d in app_names if d in entry["Name"].lower()]
                if matches:
                    print(f"{instance_id}, {entry['Name']}")


@click.command()
@click.option("--instanceid", "-i", help="EC2 instance ID. Describe all instances if not specified.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(instanceid, profile, region):
    Helper().start(profile, region, "ec2", {"instance_id": instanceid})


if __name__ == "__main__":
    main()
