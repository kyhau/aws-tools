"""
This utility script sets up aws credentials for user.
**WARNING**: This script modifies current user's aws config.
"""
from os.path import expanduser, exists, join
from os import environ, makedirs
import sys

# Check mandatory environment variable settings
ENV_AWS_ACCESS_KEY_ID = "AWS_ACCESS_KEY_ID"
ENV_AWS_SECRET_ACCESS_KEY = "AWS_SECRET_ACCESS_KEY"
for v in [ENV_AWS_ACCESS_KEY_ID, ENV_AWS_SECRET_ACCESS_KEY]:
    if v not in environ:
        print("Environment variable {} not set. Aborted.".format(v))
        sys.exit(1)

PROFILE_NAME="[k-eb-deploy]"

credential_data = [
    "",
    "# The profile {} is added by eb-app-template/deploy/setup_aws_profile.py".format(PROFILE_NAME),
    "{}".format(PROFILE_NAME),
    "aws_access_key_id = {}".format(environ[ENV_AWS_ACCESS_KEY_ID]),
    "aws_secret_access_key = {}".format(environ[ENV_AWS_SECRET_ACCESS_KEY])
]


def main():
    """Add aws profile and credential for current user.
    """
    # Prepare user specific aws config directory
    user_aws_root = join(expanduser("~"), ".aws")
    if not exists(user_aws_root):
        makedirs(user_aws_root)

    cred_file = join(user_aws_root, "credentials")
    print("Checking if profile {} exists ...".format(credential_data[2]))
    cont = True
    if exists(cred_file):
        with open(cred_file, "r") as c_file:
            if credential_data[2] in c_file.read():
                print("Profile {} exists. No change to {}.".format(credential_data[2], cred_file))
                cont = False

    if cont is True:
        with open(cred_file, "a") as c_file:
            c_file.write("\n".join(credential_data))
        print("Appended profile {} to {}.".format(credential_data[2], cred_file))


if  __name__ =="__main__": sys.exit(main())
