"""
Functions for reading/writing files
- CloudFormation template body
- json/yaml
- csv
- sql
- text
- ini
"""

import json
from os import makedirs, walk
from os.path import exists, join

import yaml


def create_dir(d):
    """Create directory if not exists."""
    makedirs(d, 0o755, exist_ok=True)


################################################################################
# CloudFormation template file


def template_body(template_file):
    with open(template_file, "r") as cf_file:
        return cf_file.read()


################################################################################
# json / yaml


def get_json_data_from_file(filename):
    """Return json object from a json or yaml file"""
    if filename.lower().endswith(".yaml"):
        with open(filename, "rb") as fp:
            yaml_data = fp.read()
            # io.BytesIO(json.dumps(yaml.load(yaml_data, Loader=yaml.FullLoader)).encode())
            return yaml.load(yaml_data, Loader=yaml.FullLoader)
    else:
        with open(filename, "r") as f:
            return json.load(f)


def write_json_file(output_file, data, sort_keys=True, indent=0):
    with open(output_file, "w") as outfile:
        json.dump(data, outfile, sort_keys=sort_keys, indent=indent)


################################################################################
# csv


def read_csv_file(filename):
    import csv

    with open(filename) as f:
        reader = csv.reader(f)
        return [list(map(str.strip, row)) for row in reader if row and not row[0].startswith("#")]


def write_csv_file(items, output_filename, delimiter=",", to_console=False):
    """
    :param items: list of list
    """
    with open(output_filename, "w") as f:
        for data in items:
            f.write(f"{delimiter.join(list(map(str, data)))}\n")
            if to_console is True:
                print(data)


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


def read_file(filename):
    with open(filename, "r") as f:
        return f.read()


def readlines_txt_file(filename):
    if filename.lower().endswith(".txt"):
        with open(filename) as f:
            lns = f.readlines()
            return [
                x.strip() for x in lns if x.strip() and not x.strip().startswith("#")
            ]  # ignore empty/commented line


################################################################################
# ini file


class IniFileHelper:
    def __init__(self):
        import configparser

        self.config = configparser.ConfigParser()

    @staticmethod
    def tokenize_multiline_values(settings, config_name, delimiter=":"):
        """Retrieve environment variables to be set for a stage"""
        env_vars = {}
        for env_var in settings.get(config_name, []):
            v = env_var.split(delimiter)
            env_vars[v[0].strip()] = v[1].strip()
        return env_vars

    @staticmethod
    def validate_file(ini_file):
        if not exists(ini_file):
            raise Exception(f"Configuration file not found: {ini_file}.")

    def get_configs_sections(self, ini_file):
        """Return list of the sections in the .ini file"""
        self.validate_file(ini_file)
        self.config.read(ini_file)
        return self.config.sections()

    def read_configs(self, ini_file, config_dict, section_list=None):
        """Retrieve settings from the ini file. Also check if any mandatory setting is missing."""
        import re

        self.validate_file(ini_file)
        self.config.read(ini_file)

        sections = ["default"]
        if section_list:
            sections.extend(section_list)

        ret = {}
        for section in sections:
            for option in self.config.options(section):
                val = self.config.get(section, option)
                if option in config_dict.keys() and config_dict[option].get("multilines") is True:
                    ret[option] = [
                        n.strip()
                        for n in re.split(";|, |\n", self.config.get(section, option))
                        if n.strip() and not n.strip().startswith("#")  # ignore commented line
                    ]
                else:
                    ret[option] = val

        passed = True
        for k, v in config_dict.items():
            if v.get("required", False) is True and ret.get(k) is None:
                print(f"Missing setting: {k}")
                passed = False
        if not passed:
            raise Exception("Missing mandatory settings in INI file. Aborted")

        return ret

    def create_ini_template(self, ini_file, app_name, config_dict, allow_overriding_default=True):
        """
        Create ini template for the given app_name
        :param ini_file: file name of the .ini file
        :param app_name: __file__ of the caller file
        :param config_dict: default settings
        :param allow_overriding_default: True if allowing other section to override
            the default section
        :raise Exception: if file already exists
        """
        if exists(ini_file):
            raise Exception(f"{ini_file} already exists. Aborted")

        lines = ["[default]\n"]
        lines.extend(
            [
                f"{k} = {v.get('default') if v.get('default') is not None else ''}\n"
                for k, v in config_dict.items()
            ]
        )

        if allow_overriding_default:
            lines.append(
                "\n# Add other section to override those in [default] (e.g. for staging)\n"
            )

        with open(ini_file, "w") as f:
            f.writelines(lines)

    def update_ini(self, ini_file, config_updates=[]):
        if exists(ini_file):
            self.config.read(ini_file)

        for c in config_updates:
            section, option, value = c

            if section not in self.config.sections():
                self.config.add_section(section)
            self.config.set(section, option, value)

        with open(ini_file, "w") as configfile:
            self.config.write(configfile)
