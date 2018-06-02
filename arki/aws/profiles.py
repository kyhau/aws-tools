import click
from os.path import expanduser, join
import sys

from arki.system import print_export_env


AWS_CONFIG_FILE = join(join(expanduser("~"), ".aws"), "config")
AWS_CREDENTIALS_FILE = join(join(expanduser("~"), ".aws"), "credentials")


def profiles(aws_config_file=AWS_CONFIG_FILE):
    """Return all AWS profiles' names in the AWS config file.
    """
    profile_list = []
    with open(aws_config_file, "r") as c_file:
        for line in c_file.readlines():
            if "profile" in line:
                profile_name = line.split("]")[0].split("profile")[1].strip()
                profile_list.append(profile_name)
    return profile_list


def credential(profile_name, aws_credentials_file=AWS_CREDENTIALS_FILE):
    """Return credential of the given profile name.
    """
    found_line_number = 0
    with open(aws_credentials_file, "r") as c_file:
        lines = c_file.readlines()
        for i in range(0, len(lines)):
            if profile_name in lines[i] and profile_name == lines[i].split("]")[0].split("[")[1].strip():
                found_line_number = i
                break
    if found_line_number == 0:
        return None

    cred = {}
    for j in range(found_line_number+1, len(lines)):
        line = lines[j]
        if "aws_access_key_id" in line:
            cred["AWS_ACCESS_KEY_ID"] = line.split("=")[1].strip()
        elif "aws_secret_access_key" in line:
            cred["AWS_SECRET_ACCESS_KEY"] = line.split("=")[1].strip()
        if len(cred) == 2:
            return cred
    return None


def check_profile_valid(input):
    """Check if the given profile name exists in the default AWS config file.
    """
    profile_list = profiles()
    try:
        profile_name = profile_list[int(input)] if input.isdigit() else input
    except Exception as e:
        print(f"Profile index {input} not found")
        return None

    profile_name = profile_name if profile_name in profile_list else None
    if profile_name is None:
        print(f"Profile {input} not found")
    return profile_name


@click.command()
@click.option("--export_key", "-e", required=False, help="Print the command to export ACCESS KEY. Valid values: The profile name or its index returned from running `aws_profiles`.")
@click.option("--export_profile", "-p", required=False, help="Print the command to export AWS_PROFILE. Valida values: The profile name or its index returned from running `aws_profiles`.")
def main(export_key, export_profile):
    """
    aws_profile returns the list of profiles specified in ~/.aws/config.
    And you can use -e or -p to print the command to export the ACCESS KEY or AWS_PROFILE
    environment variables, by specifying the profile name (e.g. aws_profile -e my_profile_1) or
    the index of the profile printed from running `aws_profile` (e.g. aws_profile -e 1).
    """
    try:
        if not export_key and not export_profile:
            profile_list = profiles()
            for i in range(0, len(profile_list)):
                print(f"{i}: {profile_list[i]}")

        else:
            if export_key:
                profile_name = check_profile_valid(export_key)
                if profile_name:
                    print_export_env(env_dict=credential(profile_name))

            if export_profile:
                profile_name = check_profile_valid(export_profile)
                if profile_name:
                    print_export_env(env_dict={"AWS_PROFILE": profile_name})

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    sys.exit(0)
