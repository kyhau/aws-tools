"""
Read in a csv file (account_id, region, function_name, profile) and
downloads the package zip file of the Lambda functions.
"""
import csv
import logging
import os
import shutil
import zipfile

import requests
from boto3.session import Session

logging.getLogger().setLevel(logging.INFO)

# account_id, region, function_name, profile
INPUT_FILE = "lambda_functions.csv"


def read_csv_file(filename):
    with open(filename) as f:
        reader = csv.reader(f)
        return [list(map(str.strip, row)) for row in reader if row and not row[0].startswith("#")]


def download_file(url, output_file):
    r = requests.get(url, verify=False, stream=True)
    r.raw.decode_content = True
    with open(output_file, "wb") as f:
        shutil.copyfileobj(r.raw, f)

def unzip_file(downloaded_zip_file, dest_folder):
    with zipfile.ZipFile(downloaded_zip_file, "r") as zip_ref:
        zip_ref.extractall(dest_folder)


def main():
    lines = read_csv_file(INPUT_FILE)
    for line in lines:
        account_id = line[0]
        region = line[1]
        function_name = line[2]
        profile = line[3]

        logging.info("---------------------------------------")
        logging.info(f"Checking {account_id} {region} {function_name}")
        logging.info(line)

        session = Session(profile_name=profile)
        resp = session.client("lambda", region_name=region).get_function(FunctionName=function_name)
        code = resp["Code"]

        if code["RepositoryType"] == "S3":
            logging.info(code["Location"])

            downloaded_zip_file = f"downloads/{account_id}/{function_name}.zip"
            os.makedirs(f"downloads/{account_id}", exist_ok=True)

            download_file(code["Location"], downloaded_zip_file)

            dest_folder = f"local/{account_id}/{function_name}"
            os.makedirs(dest_folder, exist_ok=True)
            unzip_file(downloaded_zip_file, dest_folder)

        else:
            logging.info("TODO: " + code["RepositoryType"])


if __name__ == "__main__":
    main()
