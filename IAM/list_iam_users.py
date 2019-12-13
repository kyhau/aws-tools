"""
List UserArn, CreateDate, PasswordLastUsed, AccessKeyMetadata
"""
from boto3.session import Session
import click
from configparser import ConfigParser
from os.path import expanduser, join

aws_profiles = []
try:
    cp = ConfigParser()
    cp.read(join(expanduser("~"), ".aws", "credentials"))
    aws_profiles = cp.sections()
except Exception as e:
    print(e)


def list_action(session):
    try:
        paginator = session.client("iam").get_paginator("list_users")
        for page in paginator.paginate():
            for user in page["Users"]:
                ret = session.client("iam").list_access_keys(UserName=user["UserName"])
                data = {
                    "Arn": user["Arn"],
                    "CreateData": user["CreateDate"],
                    "PasswordLastUsed": user.get("PasswordLastUsed"),
                    "AccessKeyMetadata": ret.get("AccessKeyMetadata"),
                }
                print(data)
                
    except Exception as e:
        print(e)


################################################################################
# Entry point

@click.command()
@click.option("--profile", "-p", help="AWS profile name")
@click.option("--rolesfile", "-r", help="Files containing Role ARNs")
def main(profile, rolesfile):
    
    if rolesfile:
        from arki_common.aws import assume_role, read_role_arns_from_file
        try:
            for role_arn in read_role_arns_from_file(filename=rolesfile):
                session = assume_role(role_arn=role_arn)
                list_action(session)
        except Exception as e:
            print(e)

    else:
        profile_names = [profile] if profile else aws_profiles
        
        for profile_name in profile_names:
            try:
                print(f"Checking {profile_name}")
                session = Session(profile_name=profile_name)
                list_action(session)
            except Exception as e:
                print(e)


if __name__ == "__main__": main()
