import click
import logging
from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)

instance_ids = [
]
commands_to_run = [
    "tasklist | findstr sql"
]


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        client = session.client("ssm", region_name=region)
        resp = client.send_command(**kwargs)
        command_id = resp["Command"]["CommandId"]
        logging.debug(command_id)
    
        for instance_id in instance_ids:
            output = client.get_command_invocation(
                CommandId=command_id,
                InstanceId=instance_id
            )
            print(output)


@click.command()
@click.option("--instanceid", "-i", help="EC2 instance ID")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(instanceid, profile, region):
    kwargs = {
        "InstanceIds": [instanceid] if instanceid else instance_ids,
        "DocumentName": "AWS-CheckIfSqlServerRunning",
        "Parameters": {
            "commands": commands_to_run,
        }
    }
    Helper().start(profile, region, "ssm", kwargs)


if __name__ == "__main__":
    main()
