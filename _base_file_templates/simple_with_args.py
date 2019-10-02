import boto3
from boto3.session import Session
import click
from os.path import basename

AWS_PROFILE="default"
AWS_DEFAULT_REGION="ap-southeast-2"
APP_NAME = basename(__file__).split(".")[0]

"""
import datetime
import json
from time import mktime

class DefaultEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, datetime.datetime):
      return int(mktime(obj.timetuple()))
    return json.JSONEncoder.default(self, obj)

json.dumps(json_data, cls=DefaultEncoder, sort_keys=True, indent=2)
"""

################################################################################
# Entry point

@click.command()
@click.option("--profile", "-p", default="default", help="AWS profile name")
def main(profile):
    session = Session(profile_name=profile)
    this_identity = session.client("sts").get_caller_identity()
    print(f"Started processing identity {this_identity['Arn']}")


if __name__ == "__main__": main()
