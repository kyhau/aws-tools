import configparser
import logging
from os.path import basename, expanduser, exists, join
from os import makedirs
import re
from arki import PACKAGE_NAME


ARKI_LOCAL_STORE_ROOT = join(expanduser("~"), ".arki")
ARKI_LOCAL_INI = join(ARKI_LOCAL_STORE_ROOT, "arki.ini")


makedirs(ARKI_LOCAL_STORE_ROOT, 0o755, exist_ok=True)


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


def create_ini_template(ini_file, module, config_dict, allow_overriding_default=False):
    """
    Create ini template for the given module
    :param ini_file: file name of the .ini file
    :param module: __file__ of the caller file
    :param config_dict: default settings
    :param allow_overriding_default: True if allowing other section to override the default section
    :raise Exception: if file already exists
    """
    if exists(ini_file):
        raise Exception(f"{ini_file} already exists. Aborted")

    lines = [
        f"# {PACKAGE_NAME} {basename(module).split('.')[0]} configurations\n\n",
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


def read_configs(ini_file, config_dict, section_list=None):
    """
    Retrieve settings from the ini file. Also check if any mandatory setting is missing.
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
                ret[option] = process_multi_lines_config(val)
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


def process_multi_lines_config(values_str):
    """Return list of values of multi-lines config
    """
    try:
        return [
            n.strip() for n in re.split(';| |, |\*|\n', values_str) \
            #ignore commented line
            if n.strip() and not n.strip().startswith('#')
        ]
    except Exception as e:
        logging.error(e)
    return []

