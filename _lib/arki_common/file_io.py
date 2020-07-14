"""
Functions for reading/writing files
"""
import io
import json
from os import walk
from os.path import join
import yaml


################################################################################
# CloudFormation template file

def template_body(template_file):
    with open(template_file, "r") as cf_file:
        return cf_file.read()


################################################################################
# csv

def read_csv_file(filename):
    import csv
    if filename.lower().endswith(".csv"):
        with open(filename) as csv_file:
            reader = csv.reader(csv_file)
            return [
                list(map(str.strip, row)) for row in reader if row and not row[0].startswith("#")
            ]


def write_csv_file(items, output_filename, delimiter=",", to_console=True):
    """
    :param items: list of list
    """
    with open(output_filename, "w") as f:
        for data in items:
            if to_console is True:
                print(data)
            f.write(f"{delimiter.join(list(map(str, data)))}\n")


################################################################################
# json / yaml

def get_json_data_from_file(input_file):
    """Return json object from a json or yaml file"""
    if input_file.lower().endswith(".yaml"):
        with open(input_file, "rb") as fp:
            yaml_data = fp.read()
            return io.BytesIO(json.dumps(yaml.load(yaml_data)).encode())
    else:
        with open(input_file, "r") as f:
            return json.load(f)


################################################################################
# sql

def get_sql_files(root_dir):
    sql_files = []
    for root, _, files in walk(root_dir):
        sql_files.extend(join(root, file) for file in files if file.endswith(".sql"))
    return sql_files


def read_sql_file(filename):
    with open(filename, "r") as sql_file:
        content = sql_file.read()
    return content.replace("\n", " ").replace(";", "")


################################################################################
# txt

def read_file(template_file):
    with open(template_file, "r") as cf_file:
        return cf_file.read()


def readlines_txt_file(filename):
    if filename.lower().endswith(".txt"):
        with open(filename) as f:
            lns = f.readlines()
            return [
                x.strip()
                for x in lns
                if x.strip() and not x.strip().startswith("#")
            ]  # ignore empty/commented line
