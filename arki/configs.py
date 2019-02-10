import boto3
import configparser
from functools import wraps
import logging
from os.path import basename, expanduser, exists, join
from os import makedirs
import re
import sys
import toml

from arki import (
    init_logging,
    PACKAGE_NAME,
)


ARKI_LOCAL_STORE_ROOT = join(expanduser("~"), ".arki")
ARKI_LOCAL_INI = join(ARKI_LOCAL_STORE_ROOT, "arki.toml")

makedirs(ARKI_LOCAL_STORE_ROOT, 0o755, exist_ok=True)


def default_config_file_path(filename):
    return join(ARKI_LOCAL_STORE_ROOT, filename)


class ConfigsHelper():
    def __init__(self, app_name, default_configs, config_file):
        self.app_name = app_name
        self.default_configs = default_configs
        self.config_file = config_file
        self.configs = {}

    def settings(self, config_sections):
        ret = {}

        for curr_section in config_sections:
            levels = curr_section.split(".")
            curr_section_block = self.configs
            for i in levels:
                if i not in curr_section_block:
                    raise Exception(f"Section '{i}' not found. Aborted")
                curr_section_block = curr_section_block[i]
                ret.update(curr_section_block)

        passed = True
        for k, v in self.default_configs.items():
            if v.get("required", False) is True and ret.get(k) is None:
                logging.error(f"Missing setting: {k}")
                passed = False
        if not passed:
            raise Exception("Missing mandatory settings in config file. Aborted")
        return ret

    def load_configs(self):
        self.configs = toml.load(self.config_file)

    def create_ini_template(self, allow_overriding_default=True):
        """
        Create ini template for the given app_name

        :param allow_overriding_default: True if allowing other section to override the default section
        :raise Exception: if file already exists
        """
        if exists(self.config_file):
            raise Exception(f"{self.config_file} already exists. Aborted")

        self.configs[self.app_name] = {
            k : v.get("default") if v.get("default") is not None else ""
            for k, v in self.default_configs.items()
        }

        if allow_overriding_default:
            # Add other section to override those in [default] (e.g. for staging)
            self.configs[self.app_name]["test"] = {}
            self.configs[self.app_name]["prod"] = {}

        with open(self.config_file, "w") as f:
            toml.dump(self.configs, f)
            logging.info(f"{self.config_file} created")


def init_wrapper(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        init_logging()
        logging.debug("At wrapper")
        logging.debug(kwargs)

        config_file = kwargs.get("config_file", kwargs.get("default_config_file"))
        default_configs = kwargs.get("default_configs")
        config_section = kwargs.get("config_section")
        allow_overriding_default = kwargs.get("allow_overriding_default", True)
        app_name = kwargs.get("app_name")
        return_code = 0

        try:
            helper = ConfigsHelper(app_name, default_configs, config_file)
            if exists(config_file):
                helper.load_configs()
            else:
                helper.create_ini_template(allow_overriding_default)

            settings = helper.settings(config_sections=[config_section])

            profile_name = settings.get("aws.profile")
            if profile_name:
                logging.debug(f"Set up default aws profile section: {profile_name}")
                boto3.setup_default_session(profile_name=profile_name)

            kwargs["_arki_configs"] = helper.configs
            kwargs["_arki_settings"] = settings

            logging.debug("Start running actual function")
            return_code = func(*args, **kwargs)

        except Exception as e:
            import traceback
            traceback.print_stack()
            logging.error(e)
            return_code = 1

        sys.exit(return_code)

    return wrapper


def update_ini(ini_file=ARKI_LOCAL_INI, config_updates=None):
    if not exists(ini_file):
        with open(ini_file, "w") as f:
            f.write(f"# {PACKAGE_NAME} Configurations\n\n")
            logging.info(f"{ini_file} created")

    config = configparser.ConfigParser()
    config.read(ini_file)

    for c in config_updates:
        section, option, value = c

        if section not in config.sections():
            config.add_section(section)
        config.set(section, option, value)

    with open(ini_file, "w") as configfile:
        config.write(configfile)


def create_ini_template(ini_file, app_name, config_dict, allow_overriding_default=True):
    """
    Create ini template for the given app_name
    :param ini_file: file name of the .ini file
    :param app_name: __file__ of the caller file
    :param config_dict: default settings
    :param allow_overriding_default: True if allowing other section to override the default section
    :raise Exception: if file already exists
    """
    if exists(ini_file):
        raise Exception(f"{ini_file} already exists. Aborted")

    lines = [
        f"# {PACKAGE_NAME} {basename(app_name).split('.')[0]} configurations\n\n",
        "[default]\n"
    ]
    lines.extend([
        f"{k} = {v.get('default') if v.get('default') is not None else ''}\n"
        for k, v in config_dict.items()
    ])

    if allow_overriding_default:
        lines.append("\n# Add other section to override those in [default] (e.g. for staging)\n")

    with open(ini_file, "w") as f:
        f.writelines(lines)
        logging.info(f"{ini_file} created")


def get_configs_sections(ini_file):
    """Return list of the sections in the .ini file
    """
    if not exists(ini_file):
        raise Exception(f"Configuration file not found: {ini_file}.")

    config = configparser.ConfigParser()
    config.read(ini_file)
    return config.sections()


def read_configs(ini_file, config_dict, section_list=None):
    """Retrieve settings from the ini file. Also check if any mandatory setting is missing.
    """
    if not exists(ini_file):
        raise Exception(f"Configuration file not found: {ini_file}.")

    config = configparser.ConfigParser()
    config.read(ini_file)

    sections = ["default"]
    if section_list:
        sections.extend(section_list)

    ret = {}
    for section in sections:
        for option in config.options(section):
            val = config.get(section, option)
            if option in config_dict.keys() and config_dict[option].get("multilines") is True:
                ret[option] = [
                    n.strip() for n in re.split(";|, |\n", config.get(section, option)) \
                    if n.strip() and not n.strip().startswith("#") # ignore commented line
                ]
            else:
                ret[option] = val

    passed = True
    for k, v in config_dict.items():
        if v.get("required", False) is True and ret.get(k) is None:
            logging.error(f"Missing setting: {k}")
            passed = False
    if not passed:
        raise Exception("Missing mandatory settings in INI file. Aborted")

    return ret


def tokenize_multiline_values(settings, config_name, delimiter=":"):
    """Retrieve environment variables to be set for a stage
    """
    env_vars = {}
    for env_var in settings.get(config_name, []):
        v = env_var.split(delimiter)
        env_vars[v[0].strip()] = v[1].strip()
    return env_vars