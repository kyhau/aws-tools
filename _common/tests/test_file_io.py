"""Test cases for file_io module."""

import json
from os import path

import pytest
from helper.file_io import (
    IniFileHelper,
    create_dir,
    get_json_data_from_file,
    read_csv_file,
    read_sql_file,
    readlines_txt_file,
    template_body,
    write_csv_file,
    write_json_file,
)


class TestIniFileHelper:
    """Test suite for IniFileHelper class."""

    def test_get_configs_sections(self, sample_configs_1):
        """Test getting configuration sections from INI file."""
        ini_file, _ = sample_configs_1
        ret = IniFileHelper().get_configs_sections(ini_file)
        assert ret == ["default", "dev"]

    def test_read_configs_success(self, sample_configs_1):
        """Test reading configurations successfully."""
        ini_file, default_configs = sample_configs_1
        settings = IniFileHelper().read_configs(ini_file, default_configs)

        assert settings["aws.lambda.runtime"] == "python3.6"
        assert settings["aws.lambda.timeout"] == "60"
        assert settings["aws.lambda.kmskey.arn"] == ""
        assert settings["aws.lambda.environment"] == ["x1: v1", "x2: v2"]

    def test_read_configs_with_section_list(self, sample_configs_1):
        """Test reading configs with specific sections."""
        ini_file, default_configs = sample_configs_1
        settings = IniFileHelper().read_configs(ini_file, default_configs, section_list=["dev"])

        # dev section overrides default timeout
        assert settings["aws.lambda.timeout"] == "90"

    def test_validate_file_raises_on_missing_file(self):
        """Test that validate_file raises exception for missing file."""
        with pytest.raises(Exception, match="Configuration file not found"):
            IniFileHelper.validate_file("/nonexistent/file.ini")

    def test_tokenize_multiline_values(self, sample_configs_1):
        """Test tokenizing multiline values."""
        ini_file, default_configs = sample_configs_1
        settings = IniFileHelper().read_configs(ini_file, default_configs)

        assert settings["aws.lambda.environment"] == ["x1: v1", "x2: v2"]

        var_dict = IniFileHelper.tokenize_multiline_values(settings, "aws.lambda.environment")
        assert var_dict == {"x1": "v1", "x2": "v2"}

    def test_tokenize_multiline_values_custom_delimiter(self):
        """Test tokenizing with custom delimiter."""
        settings = {"vars": ["key1=value1", "key2=value2"]}
        var_dict = IniFileHelper.tokenize_multiline_values(settings, "vars", delimiter="=")
        assert var_dict == {"key1": "value1", "key2": "value2"}

    def test_create_ini_template_success(self, unittest_workspace):
        """Test creating INI template file."""
        ini_file = path.join(unittest_workspace, "new_template.ini")
        config_dict = {
            "setting1": {"default": "value1"},
            "setting2": {"default": None},
        }

        IniFileHelper().create_ini_template(ini_file, "test_app", config_dict)

        assert path.exists(ini_file)
        with open(ini_file, "r") as f:
            content = f.read()
            assert "[default]" in content
            assert "setting1 = value1" in content
            assert "setting2 = " in content

    def test_create_ini_template_raises_if_exists(self, unittest_workspace):
        """Test that create_ini_template raises if file exists."""
        ini_file = path.join(unittest_workspace, "existing.ini")
        with open(ini_file, "w") as f:
            f.write("[default]\n")

        with pytest.raises(Exception, match="already exists"):
            IniFileHelper().create_ini_template(ini_file, "test_app", {})

    def test_update_ini_creates_new_sections(self, unittest_workspace):
        """Test that update_ini can create new sections."""
        ini_file = path.join(unittest_workspace, "update_test.ini")

        helper = IniFileHelper()
        config_updates = [
            ("newsection", "option1", "value1"),
            ("newsection", "option2", "value2"),
        ]
        helper.update_ini(ini_file, config_updates)

        assert path.exists(ini_file)
        helper2 = IniFileHelper()
        helper2.config.read(ini_file)
        assert "newsection" in helper2.config.sections()
        assert helper2.config.get("newsection", "option1") == "value1"

    def test_read_configs_raises_on_missing_required(self, unittest_workspace):
        """Test that read_configs raises when required setting is missing."""
        ini_file = path.join(unittest_workspace, "incomplete.ini")
        with open(ini_file, "w") as f:
            f.write("[default]\n")
            f.write("setting1 = value1\n")

        config_dict = {
            "setting1": {"required": True},
            "setting2": {"required": True},  # This is missing
        }

        with pytest.raises(Exception, match="Missing mandatory settings"):
            IniFileHelper().read_configs(ini_file, config_dict)


class TestFileOperations:
    """Test suite for various file operations."""

    def test_template_body(self, unittest_workspace):
        """Test reading CloudFormation template body."""
        template_file = path.join(unittest_workspace, "template.yaml")
        content = "AWSTemplateFormatVersion: '2010-09-09'\nDescription: Test"
        with open(template_file, "w") as f:
            f.write(content)

        result = template_body(template_file)
        assert result == content

    def test_get_json_data_from_json_file(self, unittest_workspace):
        """Test reading JSON data from .json file."""
        json_file = path.join(unittest_workspace, "data.json")
        data = {"key": "value", "number": 42}
        with open(json_file, "w") as f:
            json.dump(data, f)

        result = get_json_data_from_file(json_file)
        assert result == data

    def test_get_json_data_from_yaml_file(self, unittest_workspace):
        """Test reading JSON data from .yaml file."""
        yaml_file = path.join(unittest_workspace, "data.yaml")
        with open(yaml_file, "w") as f:
            f.write("key: value\nnumber: 42\n")

        result = get_json_data_from_file(yaml_file)
        assert result["key"] == "value"
        assert result["number"] == 42

    def test_write_json_file(self, unittest_workspace):
        """Test writing JSON file."""
        json_file = path.join(unittest_workspace, "output.json")
        data = {"z": 3, "a": 1, "m": 2}

        write_json_file(json_file, data, sort_keys=True, indent=2)

        assert path.exists(json_file)
        with open(json_file, "r") as f:
            loaded = json.load(f)
            assert loaded == data

    def test_read_csv_file(self, unittest_workspace):
        """Test reading CSV file."""
        csv_file = path.join(unittest_workspace, "data.csv")
        with open(csv_file, "w") as f:
            f.write("col1,col2,col3\n")
            f.write("val1,val2,val3\n")
            f.write("# comment line\n")
            f.write("val4,val5,val6\n")

        result = read_csv_file(csv_file)
        assert len(result) == 3  # Header + 2 data rows, comment filtered
        assert result[0] == ["col1", "col2", "col3"]
        assert result[1] == ["val1", "val2", "val3"]

    def test_write_csv_file(self, unittest_workspace):
        """Test writing CSV file."""
        csv_file = path.join(unittest_workspace, "output.csv")
        items = [
            ["col1", "col2", "col3"],
            ["val1", "val2", "val3"],
            [1, 2, 3],
        ]

        write_csv_file(items, csv_file, delimiter=",")

        assert path.exists(csv_file)
        with open(csv_file, "r") as f:
            lines = f.readlines()
            assert "col1,col2,col3\n" in lines
            assert "1,2,3\n" in lines

    def test_read_sql_file(self, unittest_workspace):
        """Test reading SQL file."""
        sql_file = path.join(unittest_workspace, "query.sql")
        with open(sql_file, "w") as f:
            f.write("SELECT *\nFROM table\nWHERE id = 1;")

        result = read_sql_file(sql_file)
        # Newlines should be replaced with spaces, semicolon removed
        assert "\n" not in result
        assert ";" not in result
        assert "SELECT" in result

    def test_readlines_txt_file(self, unittest_workspace):
        """Test reading text file lines."""
        txt_file = path.join(unittest_workspace, "data.txt")
        with open(txt_file, "w") as f:
            f.write("line1\n")
            f.write("line2\n")
            f.write("# comment\n")
            f.write("\n")
            f.write("line3\n")

        result = readlines_txt_file(txt_file)
        # Should filter empty lines and comments
        assert result == ["line1", "line2", "line3"]

    def test_readlines_txt_file_non_txt_returns_none(self):
        """Test that readlines_txt_file returns None for non-.txt files."""
        result = readlines_txt_file("data.csv")
        assert result is None

    def test_create_dir(self, unittest_workspace):
        """Test creating directory."""
        new_dir = path.join(unittest_workspace, "new", "nested", "dir")
        create_dir(new_dir)
        assert path.exists(new_dir)
        assert path.isdir(new_dir)

    def test_create_dir_already_exists(self, unittest_workspace):
        """Test that create_dir doesn't fail if directory exists."""
        new_dir = path.join(unittest_workspace, "existing")
        create_dir(new_dir)
        # Should not raise exception
        create_dir(new_dir)
        assert path.exists(new_dir)
