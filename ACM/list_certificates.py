"""
List certificates of account(s)
"""
import logging

import click
from helper.aws import AwsApiHelper
from helper.ser import dump_json

logging.getLogger().setLevel(logging.INFO)


class Helper(AwsApiHelper):
    def __init__(self, detailed):
        super().__init__()
        self._detailed = detailed

    def process_request(self, session, account_id, region, kwargs):
        client = session.client("acm", region_name=region)
        data_list = []
        for page in client.get_paginator("list_certificates").paginate():
            data_list.extend(page["CertificateSummaryList"])

        for data in data_list:
            item = client.describe_certificate(CertificateArn=data["CertificateArn"])["Certificate"]
            data = item if self._detailed else {
                "AccountId": account_id,
                "Region": region,
                "CertificateArn": item["CertificateArn"],
                "DomainName": item["DomainName"],
                "NotAfter": item["NotAfter"].strftime("%Y-%m-%d %H:%M:%S"),
                "InUseByCnt": len(item["InUseBy"]),
                "Issuer": item["Issuer"],
                "Status": item["Status"],
                "Type": item["Type"],
            }
            print(dump_json(data))


@click.command()
@click.option("--detailed", "-d", show_default=True, is_flag=True, help="Show all details.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(detailed, profile, region):
    Helper(detailed).start(profile, region, "acm")


if __name__ == "__main__":
    main()
