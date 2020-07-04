import click
import logging
from arki_common.aws import AwsApiHelper

logging.getLogger().setLevel(logging.DEBUG)

TARGETS = [
    "Auto Scaling Group Resources",
    "Amazon EBS Public Snapshots",
    "Amazon RDS Public Snapshots",
    "Amazon S3 Bucket Permissions",
    "CloudFront Custom SSL Certificates in the IAM Certificate Store",
    "CloudFront SSL Certificate on the Origin Server",
    "IAM Access Key Rotation",
]


class Helper(AwsApiHelper):
    def process_request(self, session, account_id, region, kwargs):
        # Trusted Advisor only works in "us-east-1" or no region
        ret = []
        client = session.client("support", region_name="us-east-1")
        for item in [x for x in client.describe_trusted_advisor_checks(language="en")["checks"] if
                     x["name"] in TARGETS]:
            result = client.describe_trusted_advisor_check_result(checkId=item["id"], language="en")["result"]
            if result["status"] in ["error", "warning"]:
                # "ok" (green), "warning" (yellow), "error" (red), "not_available"
                data = {
                    "AccountId": account_id,
                    "Category": item["category"],
                    "Id": item["id"],
                    "Name": item["name"],
                    "ResourcesFlaggedCnt": result.get("resourcesSummary", {}).get("resourcesFlagged", 0),
                    "ResourcesFlagged": result.get("flaggedResources", []),
                }
                ret.append(data)
        return ret


@click.command()
@click.option("--profile", "-p", help="AWS profile name. Use profiles in ~/.aws if not specified.")
def main(profile):
    Helper().start(profile, "us-east-1", "support")


if __name__ == "__main__":
    main()
