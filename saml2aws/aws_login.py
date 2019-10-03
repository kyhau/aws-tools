#!/usr/bin/env python3
import click
import csv
import getpass
from os.path import abspath, dirname, join
from pathlib import Path
import subprocess

SAML2AWS_CONFIG = join(str(Path.home()), ".saml2aws")

# role_arn, account_id, account_name
ROLES_FILE = join(dirname(abspath(__file__)), "data", "accounts.csv")

get_arn = lambda x: f"arn:aws:iam::{self.account_id}:role/{role}"


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
    print(f"CheckPt: Adding {profile_name}...")
    cmd = f"saml2aws login --role={role_arn} -p {profile_name} --username={uname} --password={upass} --skip-prompt"
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():
        print(line.decode("utf-8").rstrip("\r|\n"))
    retval = p.wait()
    print(f"CheckPt: Response Code {retval}")
    return retval


@click.command()
@click.option("--rolefile", "-r", default=SAML2AWS_CONFIG, help="CSV file containing details of roles")
def main(rolefile):
    configs = load_saml2aws_config(filename=rolefile)
    uname = configs.get("username")
    if uname is None:
        uname = input("Username: ")
    else:
        print(f"Username: {uname}")
    upass = getpass.getpass("Password: ")

    for item in load_csv(ROLES_FILE):
        role, account_id = item[0], item[1]
        role_arn = f"arn:aws:iam::{account_id}:role/{role}"
        run_saml2aws_login(role_arn, role, uname, upass)

if __name__ == "__main__": main()
