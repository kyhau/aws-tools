"""
List UserArn, CreateDate, PasswordLastUsed, AccessKeyMetadata
"""
import click
import logging
import yaml
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.INFO)


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        client = session.client("iam")
        for user in self.paginate(client, "list_users"):
            ret = client.list_access_keys(UserName=user["UserName"])
            data = {
                "Arn": user["Arn"],
                "CreateData": user["CreateDate"],
                "PasswordLastUsed": user.get("PasswordLastUsed"),
                "AccessKeyMetadata": ret.get("AccessKeyMetadata"),
            }
            print(yaml.dump(data, sort_keys=False))


@click.command()
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
def main(profile):
    Helper().start(profile, "ap-southeast-2", "iam")


if __name__ == "__main__":
    main()
