"""
1. List all APIGW custom domains, or
2. Lookup details of a APIGW custom domain by its domain name or regional domain name.
Also return base path mappings.
"""
import json
import logging

import click
from helper.aws import AwsApiHelper

logging.getLogger().setLevel(logging.INFO)


class Helper(AwsApiHelper):
    def __init__(self, detailed):
        super().__init__()
        self._detailed = detailed

    def process_request(self, session, account_id, region, kwargs):
        target_domain_name = kwargs.get("domain_name")
        cnt = 0

        client = session.client("apigateway", region_name=region)
        for item in self.paginate(client, "get_domain_names", kwargs):

            domain_name = item["domainName"]
            cnt += 1
            if self._detailed:
                item["base_path_mappings"] = [x for x in self.paginate(client, "get_base_path_mappings", {"domainName": domain_name})]

                print(json.dumps(item, indent=2, default=str))
            else:
                print(", ".join([
                    account_id,
                    region,
                    domain_name,
                    item.get("regionalDomainName"),
                ]))

            if target_domain_name and target_domain_name == domain_name:
                return True

        if not target_domain_name:
            logging.info(f"Number of APIGW custom domains in {account_id} {region}: {cnt}")


@click.command()
@click.option("--detailed", "-d", is_flag=True, default=False, help="Show all details.")
@click.option("--domain", "-i", help="Domain name or regional domain name. List all APIGW custom domains if not specified.")
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
@click.option("--region", "-r", default="ap-southeast-2", show_default=True, help="AWS Region. Use 'all' for all regions.")
def main(detailed, domain, profile, region):
    kwargs = {"domainName": domain} if domain else {}
    Helper(detailed).start(profile, region, "apigateway", kwargs)


if __name__ == "__main__":
    main()
