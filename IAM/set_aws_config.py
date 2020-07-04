"""
This utility script adds/updates aws config for user .
- WARNING: This script modifies current user's aws config.
"""
from os.path import expanduser, exists, join
from os import environ, makedirs
import sys


credential_data = [
    "",
    "# The following profile is added by set_aws_config.py",
    "[default_ci_profile]",
    f"aws_access_key_id = {environ.get('ACCESS_KEY')}",
    f"aws_secret_access_key = {environ.get('ACCESS_SECRET')}",
]


def main():
    """Add aws profile and credential for current user.
    """
    # Prepare user specific aws config directory
    user_aws_root = join(expanduser("~"), ".aws")
    if not exists(user_aws_root):
        makedirs(user_aws_root)

    cred_file = join(user_aws_root, "credentials")
    print(f"Checking if profile {credential_data[2]} exists ...")
    cont = True
    if exists(cred_file):
        with open(cred_file, "r") as c_file:
            if credential_data[2] in c_file.read():
                print(f"Profile {credential_data[2]} exists. No change to {cred_file}.")
                cont = False

    if cont is True:
        with open(cred_file, "a") as c_file:
            c_file.write("\n".join(credential_data))
        print(f"Appended profile {credential_data[2]} to {cred_file}.")


if  __name__ =="__main__":
    sys.exit(main())
