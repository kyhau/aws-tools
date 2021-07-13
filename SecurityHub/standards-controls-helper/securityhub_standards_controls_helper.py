"""
This script supports
- retrieving current Standard Controls from AWS account and generate a summary for comparison.
- taking a json file containing the expected standard controls to be enabled/disabled.

Example file content:
{
    "ACM.1": {
        "Regions": {
            "ap-south-1": {
                "ControlStatus": "ENABLED",
                "DisabledReason": ""
            },
            "ap-southeast-2": {
                "ControlStatus": "DISABLED",
                "DisabledReason": "Not Required ..."
            },
            ...
    }
}
"""
import json
import logging
import time

import boto3
import click

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)

LATEST_CONTROL_SUMMARY_OUTPUT_FILE_SUFFIX = "-New.json"

STANDARD_SUBSCRIPTIONS = {
    "aws-foundational-security-best-practices-v-1.0.0": "aws-foundational-security-best-practices/v/1.0.0",
    "cis-aws-foundations-benchmark-v-1.2.0": "cis-aws-foundations-benchmark/v/1.2.0",
}


def control_arn(region, account_id, subscription, control_id):
    _control_id = control_id.replace("CIS.", "") if subscription.startswith("cis-aws-foundations-benchmark") else control_id
    return f"arn:aws:securityhub:{region}:{account_id}:control/{STANDARD_SUBSCRIPTIONS[subscription]}/{_control_id}"


def subscription_arn(region, account_id, subscription):
    return f"arn:aws:securityhub:{region}:{account_id}:subscription/{STANDARD_SUBSCRIPTIONS[subscription]}"


def get_standards_controls(account_id, region, subscription):
    client = boto3.client("securityhub", region_name=region)
    kwargs = {"StandardsSubscriptionArn": subscription_arn(region, account_id, subscription)}
    ret = []

    resp = client.describe_standards_controls(**kwargs)
    kwargs["NextToken"] = resp.get("NextToken")
    ret.extend(resp["Controls"])
    while kwargs["NextToken"]:
        resp = client.describe_standards_controls(**kwargs)
        kwargs["NextToken"] = resp.get("NextToken")
        ret.extend(resp["Controls"])

    return ret


class StandardsControlsUpdateHelper():
    def __init__(self, subscription, region):
        self.account_id = boto3.client("sts").get_caller_identity()["Account"]
        self.region = region
        self.subscription = subscription
        self.existing_controls = self.get_existing_controls(self.account_id, region, subscription)

    @staticmethod
    def get_existing_controls(account_id, region, subscription):
        control_list = get_standards_controls(account_id, region, subscription)
        return {control["ControlId"]: control for control in control_list}

    def update_standards_controls(self, controls_settings, dry_run):
        client = boto3.client("securityhub", region_name=self.region)
        change_cnt = 0

        for control_id, control_info in controls_settings.items():
            try:
                new_control = control_info["Regions"].get(self.region)
                if new_control is None:
                    continue

                existing_control = self.existing_controls.get(control_id)
                if existing_control is None:
                    logging.warning(f"The control {control_id} is not supported in {self.region}. Skipped.")
                    continue

                if existing_control["ControlStatus"] == new_control["ControlStatus"]:
                    continue  # No need to update

                change_cnt += 1
                kwargs = {
                    "StandardsControlArn": control_arn(self.region, self.account_id, self.subscription, control_id),
                    "ControlStatus": new_control["ControlStatus"],
                }
                if new_control["ControlStatus"] == "DISABLED":
                    reason = new_control.get("DisabledReason")
                    kwargs["DisabledReason"] = reason if reason else "Not Required"

                if dry_run is True:
                    logging.info(f"Will update {kwargs} in {self.region}")
                else:
                    # Note: update_standards_control has RateLimit = 1 request per second and BurstLimit = 5 requests per second.
                    logging.info(f"Updating {kwargs} in {self.region}")
                    client.update_standards_control(**kwargs)
                    time.sleep(1)

            except client.exceptions.ResourceNotFoundException as e:
                logging.info(f"The control {control_id} is not supported in {self.region}: {e}")

            except Exception as e:
                logging.error(f"Unable to update {control_id} in {self.region}: {e}")
                import traceback
                traceback.print_exc()

        logging.info(f"Number of changes: {change_cnt}")
        return change_cnt

    def update_standard_control(self, control_id, to_enable, reason=None):
        client = boto3.client("securityhub", region_name=self.region)
        kwargs = {
            "StandardsControlArn": control_arn(self.region, self.account_id, self.subscription, control_id),
            "ControlStatus": "ENABLED" if to_enable else "DISABLED",
        }
        if to_enable is False:
            kwargs["DisabledReason"] = reason if reason else "Not Required"

        logging.info(f"Updating {kwargs} in {self.region}")
        client.update_standards_control(**kwargs)


class StandardsControlsSummaryBuilder():
    def __init__(self, subscription):
        self.controls = {}
        self.subscription = subscription
        self.account_id = boto3.client("sts").get_caller_identity()["Account"]

    def add_control_info(self, item, region):
        if item["ControlId"] not in self.controls:
            self.controls[item["ControlId"]] = {"Title": item["Title"], "Regions": {}}

        control = self.controls[item["ControlId"]]
        control["Regions"].update({region: {key: item.get(key, "") for key in ["ControlStatus", "DisabledReason"]}})

    def retrieve_controls_info(self, region):
        items = get_standards_controls(self.account_id, region, self.subscription)
        for item in items:
            self.add_control_info(item, region)


@click.group(invoke_without_command=False, help="Security Hub Standards Controls Helper")
def main_cli():
    pass


@main_cli.command(help="Update one Standards Control")
@click.option("--control-id", "-c", required=True, help="Standards Controls ID e.g. Lambda.4.")
@click.option("--enable", "-e", is_flag=True, show_default=True, help="Enable control.")
@click.option("--disable-reason", "-d", help="Disable reason.")
@click.option("--region", "-r", default="ap-southeast-2", required=True, help="AWS Region.")
@click.option("--subscription", "-s", required=True, type=click.Choice(list(STANDARD_SUBSCRIPTIONS.keys()), case_sensitive=False))
def update_control(control_id, enable, disable_reason, region, subscription):
    StandardsControlsUpdateHelper(subscription, region).update_standard_control(control_id, enable, disable_reason)


@main_cli.command(help="Update Standards Controls")
@click.option("--dry-run", "-d", is_flag=True, show_default=True, help="Dry run, no functional change.")
@click.option("--input-file", "-f", required=True, help="Standards Controls Input File (json).")
@click.option("--region", "-r", default="ap-southeast-2", required=True, help="AWS Region.")
@click.option("--subscription", "-s", required=True, type=click.Choice(list(STANDARD_SUBSCRIPTIONS.keys()), case_sensitive=False))
def update(dry_run, input_file, region, subscription):
    # Read input file
    with open(input_file, "r") as f:
        controls_settings = json.load(f)

    # Update standards controls if required
    StandardsControlsUpdateHelper(subscription, region).update_standards_controls(controls_settings, dry_run)


@main_cli.command(help="Create summary file of Standards Controls for the given regions")
@click.option("--subscription", "-s", required=True, type=click.Choice(list(STANDARD_SUBSCRIPTIONS.keys()), case_sensitive=False))
@click.option("--regions", "-r", default="ap-southeast-2", show_default=True, help="AWS Regions separated with commas.")
def summary(subscription, regions):
    helper = StandardsControlsSummaryBuilder(subscription)

    for aws_region in map(str.strip, regions.split(",")):
        try:
            helper.retrieve_controls_info(aws_region)
        except Exception:
            import traceback
            traceback.print_exc()

    output_file = f"{subscription}{LATEST_CONTROL_SUMMARY_OUTPUT_FILE_SUFFIX}"
    with open(output_file, "w") as f:
        json.dump(helper.controls, f, indent=2, default=str, sort_keys=True)


if __name__ == "__main__":
    main_cli()
