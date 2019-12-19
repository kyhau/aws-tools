#!/usr/bin/env python3
import click
from collections import OrderedDict
from configparser import ConfigParser
import csv
import getpass
import logging
from os.path import abspath, dirname, exists, join
from pathlib import Path
from PyInquirer import style_from_dict, Token, prompt
import subprocess

logging.basicConfig(format="%(message)s")
logging.getLogger().setLevel(logging.INFO)

AWS_CRED = join(str(Path.home()), ".aws", "credentials")
SAML2AWS_CONFIG = join(str(Path.home()), ".saml2aws")

# role_arn, account_name
ALL_ROLES_FILE = join(dirname(abspath(__file__)), "data", "roles_all.csv")
LAST_SELECTED_FILE = join(dirname(abspath(__file__)), "data", "aws_login_last_selected.txt")

custom_style = style_from_dict({
    Token.Separator: "#6C6C6C",
    Token.QuestionMark: "#FF9D00 bold",
    Token.Selected: "#5F819D",
    Token.Pointer: "#FF9D00 bold",
    Token.Instruction: "",  # default
    Token.Answer: "#5F819D bold",
    Token.Question: "",
})


def profile_selection(profiles):
    return [{
        "choices": profiles,
        "message": "Please choose the profile",
        "name": "profile",
        "type": "list",
    }]


def roles_selection(roles, last_selected_profiles):
    return [{
        "choices": [dict({
            "name": role,
            "checked": True if role in last_selected_profiles else False}
        ) for role in roles],
        "message": "Please choose the role",
        "name": "roles",
        "type": "checkbox",
    }]


def write_csv(output_filename, data_list):
    with open(output_filename, "w") as f:
        csv_out = csv.writer(f)
        for item in data_list:
            csv_out.writerow(item)


def read_csv(filename, delimiter=","):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for row in reader:
            if row and not row[0].startswith("#"):
                yield row


def read_lines_from_file(filename):
    if exists(filename):
        with open(filename) as f:
            content = f.readlines()
        return [x.strip() for x in content]
    return []


def load_saml2aws_config(filename):
    configs = {}
    rows = read_csv(filename, "=")
    for row in rows:
        w = [f.strip() for f in row]
        if len(w) > 1 and w[1]:
            configs[w[0]] = w[1]
    return configs


def get_aws_profiles(filename=AWS_CRED):
    cp = ConfigParser()
    cp.read(filename)
    return cp


def write_aws_profiles(config, filename=AWS_CRED):
    with open(filename, "w") as configfile:
        config.write(configfile)


def get_credentials():
    configs = load_saml2aws_config(filename=SAML2AWS_CONFIG)
    uname = configs.get("username")
    if uname is None:
        uname = input("Username: ")
    else:
        logging.info(f"Username: {uname}")
    upass = getpass.getpass("Password: ")
    return uname, upass


def run_saml2aws_login(role_arn, profile_name, uname, upass, session_duration):
    logging.info(f"Adding {profile_name}...")
    
    cmd = f"saml2aws login --role={role_arn} -p {profile_name} --username={uname} --password={upass} --skip-prompt"
    if session_duration:
        cmd = f"{cmd} --session-duration={session_duration}"
    
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        logging.debug(line.decode("utf-8").rstrip("\r|\n"))
    retval = p.wait()
    
    logging.info(f"Response Code {retval}")
    return retval


def run_saml2aws_list_roles(uname, upass):
    roles = []
    accounts_dict = {}
    
    cmd = f"saml2aws list-roles --username={uname} --password={upass} --skip-prompt"
    
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        line = line.decode("utf-8").rstrip("\r|\n")
        logging.debug(line)
        if line.startswith("Account:"):
            acc_name, acc_id = line.replace("(", "").replace(")", "").split(" ")[1:]
            accounts_dict[acc_id] = acc_name
        elif line.startswith("arn:"):
            acc_id = line.split(":")[4]
            roles.append([line, accounts_dict[acc_id]])
    retval = p.wait()
    
    logging.info(f"Response Code {retval}")
    return roles


@click.command()
@click.option("--keyword", "-k", help="Pre-select roles with the given keyword")
@click.option("--refresh-cached-roles", "-r", is_flag=True)
@click.option("--session-duration", "-t", help="Session duration in seconds")
@click.option("--switch-profile", "-s", is_flag=True)
@click.option("--debug", "-d", is_flag=True)
def main(keyword, refresh_cached_roles, session_duration, switch_profile, debug):
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if switch_profile is True:
        config = get_aws_profiles()
        options = [profile for profile in config.sections() if profile != "default"]
        if options:
            answer = prompt(profile_selection(options), style=custom_style)
            profile = answer.get("profile")
            if profile is not None:
                config["default"] = config[profile]
                write_aws_profiles(config)
                logging.info(f"Set the default profile to {profile}")
            else:
                logging.info("Nothing selected. Aborted.")
        else:
            logging.info("No non default aws profile found. Aborted.")
        return
    
    last_selected_profiles = read_lines_from_file(LAST_SELECTED_FILE)
    uname, upass = None, None
    
    if refresh_cached_roles or not exists(ALL_ROLES_FILE):
        uname, upass = get_credentials()
        roles = run_saml2aws_list_roles(uname, upass)
        write_csv(ALL_ROLES_FILE, roles)
    else:
        roles = read_csv(ALL_ROLES_FILE)
    
    profiles = OrderedDict()
    for item in roles:
        role_arn, account_name = item[0], item[1]
        profile_name = role_arn.split("role/")[-1].replace("/", "-")
        profiles[profile_name] = role_arn
        
        if keyword is not None and keyword in role_arn:
            last_selected_profiles.append(profile_name)
    
    answers = prompt(roles_selection(profiles.keys(), last_selected_profiles), style=custom_style)
    if answers.get("roles"):
        if uname is None:
            uname, upass = get_credentials()
        
        for profile_name in answers["roles"]:
            run_saml2aws_login(profiles[profile_name], profile_name, uname, upass, session_duration)

        # Dump the last selected options
        with open(LAST_SELECTED_FILE, "w") as f:
            f.write("\n".join(answers["roles"]))
    else:
        logging.info("Nothing selected. Aborted.")


if __name__ == "__main__": main()
