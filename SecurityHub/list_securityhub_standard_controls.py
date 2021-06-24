"""
Print current control status of Security Hub.
- Print "ControlId: ControlStatus" of a standard control by default.
- Print all details when `--detailed` is used.
"""
import json
import logging

import click
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)


STANDARD_SUBSCRIPTIONS = {
    "aws-foundational-security-best-practices-v-1.0.0": "aws-foundational-security-best-practices/v/1.0.0",
    "cis-aws-foundations-benchmark-v-1.2.0": "cis-aws-foundations-benchmark/v/1.2.0",
}


class Helper(AwsApiHelper):
    def __init__(self, subscription, detailed):
        super().__init__()
        self._subscription = subscription
        self._detailed = detailed

    def process_request(self, session, account_id, region, kwargs):
        kwargs["StandardsSubscriptionArn"] = f"arn:aws:securityhub:{region}:{account_id}:subscription/{self._subscription}"

        client = session.client("securityhub", region_name=region)
        resp = client.describe_standards_controls(**kwargs)
        next_token = resp.get("NextToken")
        for item in resp["Controls"]:
            self.printline(item)

        while next_token:
            kwargs["NextToken"] = next_token
            resp = client.describe_standards_controls(Expression=self._sql_statement)
            next_token = resp.get("NextToken")
            for item in resp["Controls"]:
                self.printline(item)

    def printline(self, item):
        if self._detailed:
            print(json.dumps(item, indent=2, default=str))
        else:
            print(f"{item['ControlId']}: {item['ControlStatus']}")


@click.command()
@click.option("--detailed", "-d", show_default=True, is_flag=True)
@click.option('--subscription', required=True, type=click.Choice(list(STANDARD_SUBSCRIPTIONS.keys()), case_sensitive=False))
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(detailed, subscription, profile, region):
    Helper(STANDARD_SUBSCRIPTIONS[subscription], detailed).start(profile, region, "securityhub", kwargs={})


if __name__ == "__main__":
    main()
