"""
Read in a csv file (LayerVersionArn, AccountId, Region, LayerName, CompatibleRuntimes, ProfileName) and
downloads the package zip file of the Lambda layers.
"""
import csv
import logging
import os
import shutil
import zipfile

import requests
from boto3.session import Session

logging.getLogger().setLevel(logging.INFO)

# account_id, region, layer_name, profile
INPUT_FILE = "lambda_layers.csv"


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
        layer_arn = line[0]
        account_id = line[1]
        region = line[2]
        layer_name = line[3]
        layer_runtime_list = line[4]
        profile = line[5]

        print("---------------------------------------")
        print(f"Checking {layer_arn} {layer_name} {layer_runtime_list}")
        print(line)

        session = Session(profile_name=profile)

        client = session.client("lambda", region_name=region)
        resp = client.get_layer_version_by_arn(Arn=layer_arn)

        code_location = resp["Content"]["Location"]
        print(code_location)

        downloaded_zip_file = f"downloads/layers/{account_id}/{layer_name}.zip"
        os.makedirs(f"downloads/layers/{account_id}", exist_ok=True)

        download_file(code_location, downloaded_zip_file)

        dest_folder = f"local/layers/{account_id}/{layer_name}"
        os.makedirs(dest_folder, exist_ok=True)
        unzip_file(downloaded_zip_file, dest_folder)


if __name__ == "__main__":
    main()
