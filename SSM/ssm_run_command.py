import click
import logging
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)

documents = {
    "AWS-CheckIfSqlServerRunning": {
        "commands_to_run": [
            "tasklist | findstr sql"
        ]
    }
}


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        client = session.client("ssm", region_name=region)
        resp = client.send_command(**kwargs)
        command_id = resp["Command"]["CommandId"]
        logging.debug(command_id)

        for instance_id in kwargs["InstanceIds"]:
            output = client.get_command_invocation(
                CommandId=command_id,
                InstanceId=instance_id
            )
            print(output)


@click.command()
@click.option("--document", "-d", help="Document name", required=True)
@click.option("--instanceid", "-i", help="EC2 instance ID", required=True)
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(document, instanceid, profile, region):
    kwargs = {
        "InstanceIds": [instanceid],
        "DocumentName": document,
        "Parameters": {
            "commands": documents[document],
        }
    }
    Helper().start(profile, region, "ssm", kwargs)


if __name__ == "__main__":
    main()
