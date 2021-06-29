import json
import logging

import click
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)

POLICY_FILTERS = [
    "SERVICE_CONTROL_POLICY",
    "TAG_POLICY",
    "BACKUP_POLICY",
    "AISERVICES_OPT_OUT_POLICY",
]

class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        try:
            # 1) Retrieve account id and alias at the (individual) account level. AWS supports only one alias per account
            policies = session.client("organizations", region_name=region).list_policies(**kwargs)["Policies"]
            for policy in policies:
                print(json.dumps(policy, indent=2))
        except Exception as e:
            logging.error(e)


@click.command()
@click.option("--policy-type", "-t", default=POLICY_FILTERS[0], show_default=True, type=click.Choice(POLICY_FILTERS, case_sensitive=False))
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
def main(profile, policy_type):
    Helper().start(profile, region="us-east-1", service="organizations", kwargs={"Filter": policy_type.upper()})


if __name__ == "__main__":
    main()
