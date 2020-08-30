from helper.file_io import IniFileHelper


def test_get_configs_sections_passed(sample_configs_1):
    """Test get_configs_sections passed
    """
    ini_file, _ = sample_configs_1
    ret = IniFileHelper().get_configs_sections(ini_file)
    assert ret == ["default", "dev"]


def test_read_configs_passed(sample_configs_1):
    """Test read_configs passed
    """
    ini_file, default_configs = sample_configs_1

    settings = IniFileHelper().read_configs(ini_file, default_configs)

    assert settings["aws.lambda.runtime"] == "python3.6"
    assert settings["aws.lambda.timeout"] == "60"
    assert settings["aws.lambda.kmskey.arn"] == ""
    assert settings["aws.lambda.environment"] == ["x1: v1", "x2: v2"]


def test_tokenize_multiline_values_passed(sample_configs_1):
    """Test tokenize_multiline_values passed
    """
    ini_file, default_configs = sample_configs_1
    settings = IniFileHelper().read_configs(ini_file, default_configs)

    assert settings["aws.lambda.environment"] == ["x1: v1", "x2: v2"]

    var_dict = IniFileHelper.tokenize_multiline_values(settings, "aws.lambda.environment")
    assert var_dict == {
        "x1": "v1",
        "x2": "v2"
    }
