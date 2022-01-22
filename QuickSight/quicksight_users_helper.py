"""
A simple script outputs all user names and ARNs to console and file.
"""
import json
import logging

import click
from boto3.session import Session

logging.getLogger().setLevel(logging.DEBUG)
logging.getLogger("botocore").setLevel(logging.CRITICAL)
logging.getLogger("boto3").setLevel(logging.CRITICAL)
logging.getLogger("urllib3.connectionpool").setLevel(logging.CRITICAL)


@click.command(help="Output all user names and ARNs to console and file")
@click.option("--keyword", "-k", help="Keyword in names")
@click.option("--profile", "-p", default="default", show_default=True, help="AWS profile name")
def main(keyword, profile):
    session = Session(profile_name=profile)
    client = session.client("quicksight", region_name="us-east-1")
    account_id = session.client("sts").get_caller_identity()["Account"]

    ret = {}
    params = {"AwsAccountId": account_id, "Namespace": "default"}
    while True:
        resp = client.list_users(**params)
        for r in resp["UserList"]:
            if keyword is None or keyword.lower() in r["UserName"].lower():
                ret[r["UserName"]] = r
        if resp.get("NextToken") is None:
            break
        params["NextToken"] = resp["NextToken"]

    with open("quicksight_users.json", "w") as f:
        json.dump(ret, f, indent=2, sort_keys=True)

    print(json.dumps(ret, indent=2, sort_keys=True))
    logging.info(f"Total num of Users: {len(ret)}")


if __name__ == "__main__":
     main()

