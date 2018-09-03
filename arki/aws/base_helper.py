import boto3
from arki.configs import create_ini_template, read_configs
from arki import init_logging


class BaseHelper():

    def __init__(self, default_configs, ini_file, stage_section=None):
        """

        :param default_configs: 
        :param ini_file: 
        :param stage_section: 
        """
        init_logging()
        self.default_configs = default_configs
        self.ini_file = ini_file
        self.settings = self._read_configs(stage_section)
        
        profile_name = self.settings.get("aws.profile")
        if profile_name is not None:
            boto3.setup_default_session(profile_name=profile_name)

    def _read_configs(self, stage_section):
        """

        :param stage_section:
        :return:
        """
        if self.ini_file is None:
            return {}

        return read_configs(
            ini_file=self.ini_file,
            config_dict=self.default_configs,
            section_list=[stage_section] if stage_section else None
        )

    def _create_ini_template(self, module, allow_overriding_default=True):
        """

        :param module:
        :param allow_overriding_default:
        :return:
        """
        create_ini_template(
            ini_file=self.ini_file,
            module=module,
            config_dict=self.default_configs,
            allow_overriding_default=allow_overriding_default
        )
