#!/usr/bin/env python3
import click
import csv
import getpass
import logging
from os.path import abspath, dirname, join
from pathlib import Path
import subprocess

logging.basicConfig(format="%(message)s")
logging.getLogger().setLevel(logging.INFO)

SAML2AWS_CONFIG = join(str(Path.home()), ".saml2aws")

# role_arn, account_name
ROLES_FILE = join(dirname(abspath(__file__)), "data", "roles.csv")
ALL_ROLES_FILE = join(dirname(abspath(__file__)), "data", "roles_all.csv")


def load_csv(filename, delimiter=","):
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for row in reader:
            if row and not row[0].startswith("#"):
                yield row


def load_saml2aws_config(filename):
    configs = {}
    rows = load_csv(filename, "=")
    for row in rows:
        w = [f.strip() for f in row]
        if len(w) > 1 and w[1]:
            configs[w[0]] = w[1]
    return configs


def run_saml2aws_login(role_arn, profile_name, uname, upass):
    logging.info(f"Adding {profile_name}...")
    cmd = f"saml2aws login --role={role_arn} -p {profile_name} --username={uname} --password={upass} --skip-prompt"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        logging.debug(line.decode("utf-8").rstrip("\r|\n"))
    retval = p.wait()
    logging.info(f"Response Code {retval}")
    return retval


@click.command()
@click.option("--keyword", "-k", help="Login only to roles with the given keyword")
@click.option("--debug", "-d", is_flag=True)
def main(keyword, debug):
    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    configs = load_saml2aws_config(filename=SAML2AWS_CONFIG)
    uname = configs.get("username")
    if uname is None:
        uname = input("Username: ")
    else:
        logging.info(f"Username: {uname}")
    upass = getpass.getpass("Password: ")
    
    rolefile = ALL_ROLES_FILE if keyword else ROLES_FILE
    
    for item in load_csv(rolefile):
        role_arn, account_name = item[0], item[1]
        
        if keyword is None or keyword in role_arn:
            profile_name = role_arn.split("role/")[-1].replace("/", "-")
            run_saml2aws_login(role_arn, profile_name, uname, upass)


if __name__ == "__main__": main()
