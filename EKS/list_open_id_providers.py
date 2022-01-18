"""
Print list of:
{
  "Url": "oidc.eks.ap-southeast-2.amazonaws.com/id/...",
  "ClientIDList": [
    "sts.amazonaws.com"
  ],
  "ThumbprintList": [
    ...
  ],
  "CreateDate": "2021-10-15 01:54:02.659000+00:00",
  "Tags": [
    {
      "Key": "alpha.eksctl.io/eksctl-version",
      "Value": ...
    },
    {
      "Key": "alpha.eksctl.io/cluster-name",
      "Value": ...
    }
  ],
  "FoundClusterInAccount": true,
  "ClusterName": ...,
  "ClusterStatus": "ACTIVE"
}
"""
import json
import logging

import click
from botocore.exceptions import ClientError
from helper.aws import AwsApiHelper
from helper.file_io import write_csv_file

logging.getLogger().setLevel(logging.DEBUG)


class Helper(AwsApiHelper):
    def process_account(self, session, account_id, aws_region, service, kwargs):
        results = []

        for region in session.get_available_regions(service) if aws_region == "all" else [aws_region]:
            try:
                logging.debug(f"Checking {account_id} {region}")

                eks_client = session.client("eks", region_name=region)

                # Retrieve all eks cluster names
                cluster_names = []
                for page in eks_client.get_paginator("list_clusters").paginate().result_key_iters():
                    cluster_names.extend([item for item in page])

                # Retrieve all eks clusters' oidc issues and cluster's status
                oidc_issuers = {}
                for cluster_name in cluster_names:
                    cluster = eks_client.describe_cluster(name=cluster_name)["cluster"]
                    oidc_issuers[cluster["identity"]["oidc"]["issuer"].replace("https://", "")] = {
                        "name": cluster_name,
                        "status": cluster["status"]
                    }

                # Retrieve all oidc providers
                iam_client = session.client("iam", region_name=region)
                for provider in iam_client.list_open_id_connect_providers()["OpenIDConnectProviderList"]:
                    details = iam_client.get_open_id_connect_provider(OpenIDConnectProviderArn=provider["Arn"])

                    details["FoundClusterInAccount"] = details["Url"] in oidc_issuers
                    if details["Url"] in oidc_issuers:
                        details["ClusterName"] = oidc_issuers[details["Url"]]["name"]
                        details["ClusterStatus"] = oidc_issuers[details["Url"]]["status"]

                    del details["ResponseMetadata"]
                    print(json.dumps(details, default=str))

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
    Helper().start(profile, region, "iam")


if __name__ == "__main__":
    main()
