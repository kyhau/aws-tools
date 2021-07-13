"""
This script supports
- reading policy files (json) in the specified folder, and
- comparing current SCPs against the expected policies and managing SCPs accordingly
"""
import json
import logging
import os

import boto3
import click

logging.getLogger().setLevel(logging.INFO)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)


class PolicyHelper():
    def __init__(self, region, tags):
        self.client = boto3.client("organizations", region_name=region)
        self.tags = tags

    def get_policies_from_files(self, input_dir):
        """Return dict of {policy-name-lower-case: policy-in-json}"""
        policy_dict = {}
        for filename in os.listdir(input_dir):
            if filename.endswith(".json"):
                with open(os.path.join(input_dir, filename), "r") as f:
                    policy_dict[filename.replace(".json", "").lower()] = json.load(f)
        return policy_dict

    def get_customer_managed_scp_ids(self):
        """Return a list of SCP IDs of the existing customer managed SCPs"""
        scp_list = []

        params = {"Filter": "SERVICE_CONTROL_POLICY"}
        for page in self.client.get_paginator("list_policies").paginate(**params).result_key_iters():
            scp_list.extend([item["Id"] for item in page if item["AwsManaged"] is False])

        return scp_list

    def get_customer_managed_scps(self, scp_ids):
        """Return a dict of {policy_name: policy_dict} of the existing customer managed SCPs"""
        scps = {}
        for id in scp_ids:
            resp = self.client.describe_policy(PolicyId=id)["Policy"]
            scps[resp["PolicySummary"]["Name"]] = resp
        return scps

    def create_scp(self, input_policy_name, input_policy):
        self.client.create_policy(
            Content=json.dumps(input_policy),
            Description=input_policy_name,
            Name=input_policy_name,
            Type="SERVICE_CONTROL_POLICY",
            Tags=self.tags,
        )

    def update_scp(self, curr_policy_ref, input_policy):
        self.client.update_policy(
            PolicyId=curr_policy_ref["Id"],
            Name=curr_policy_ref["Name"],
            Description=curr_policy_ref["Name"],
            Content=json.dumps(input_policy),
        )

    def manage_scps(self, input_dir, dry_run):
        # Retrieve input policies from file
        input_policies = self.get_policies_from_files(input_dir)

        # Retrieve {policy_name: policy_dict} of the existing customer managed SCPs
        curr_scps = self.get_customer_managed_scps(self.get_customer_managed_scp_ids())

        cnt_add, cnt_update, cnt_delete = 0, 0, 0

        for input_policy_name, input_policy in input_policies.items():
            if input_policy_name in curr_scps.keys():
                logging.info(f"Checking existing SCP {input_policy_name}")

                input_policy_content = json.dumps(input_policy, sort_keys=True)
                curr_policy_content = json.dumps(json.loads(curr_scps[input_policy_name]["Content"]), sort_keys=True)

                if input_policy_content == curr_policy_content:
                    logging.info("No change")
                else:
                    cnt_update += 1
                    logging.info("Change detected. Update SCP")
                    if dry_run is False:
                        self.update_scp(curr_scps[input_policy_name]["PolicySummary"], input_policy)
            else:
                cnt_add += 1
                logging.info(f"Add new SCP {input_policy_name}")
                if dry_run is False:
                    self.create_scp(self, input_policy_name, input_policy)

        for curr_policy_name in curr_scps:
            if curr_policy_name not in input_policies:
                cnt_delete += 1
                logging.info(f"Delete existing SCP {curr_policy_name}")
                if dry_run is False:
                    self.client.delete_policy(PolicyId=curr_scps[input_policy_name]["PolicySummary"]["Id"])

        logging.info(f"Total Add: {cnt_add}")
        logging.info(f"Total Delete: {cnt_delete}")
        logging.info(f"Total Update: {cnt_update}")


def get_list_from_multi_option_parameter(multi_option_parameter, key_name="Key", value_name="Value"):
    items = []
    if multi_option_parameter:
        for item in multi_option_parameter:
            key, value = list(map(str.strip, item.split(":", 1)))
            items.append({key_name: key, value_name: value})
    return items


@click.command(help="Update SCPs")
@click.option("--dry-run", "-d", is_flag=True, show_default=True, help="Dry run, no functional change.")
@click.option("--input-dir", "-i", required=True, help="Path to directory containing policy files.")
@click.option("--region", "-r", help="AWS Region.")
@click.option('--tag', '-t', multiple=True, help="Format name:value.")
def main(dry_run, input_dir, region, tag):
    # `tag` is "multiple option"
    tags = get_list_from_multi_option_parameter(tag)
    logging.info(tags)

    PolicyHelper(region, tags).manage_scps(input_dir, dry_run)


if __name__ == "__main__":
    main()
