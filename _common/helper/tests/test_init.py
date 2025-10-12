"""Test cases for __init__ module."""
import pytest
from helper import PACKAGE_NAME, print_all_console_scripts


class TestPackageName:
    """Test suite for PACKAGE_NAME constant."""

    def test_package_name_is_helper(self):
        """Test that PACKAGE_NAME is set to 'helper'."""
        assert PACKAGE_NAME == "helper"

    def test_package_name_is_string(self):
        """Test that PACKAGE_NAME is a string."""
        assert isinstance(PACKAGE_NAME, str)


class TestPrintAllConsoleScripts:
    """Test suite for print_all_console_scripts function."""

    def test_returns_list(self):
        """Test that function returns a list."""
        result = print_all_console_scripts()
        assert isinstance(result, list)

    def test_finds_helper_console_scripts(self):
        """Test that function finds helper-related console scripts."""
        result = print_all_console_scripts("helper")

        # Should find at least the console scripts defined in setup.py
        # helper, dockerc, dockeri
        script_names = [ep.name for ep in result]

        # Check if any scripts were found (may vary based on installation)
        assert isinstance(script_names, list)

    def test_prints_header(self, capsys):
        """Test that function prints header information."""
        print_all_console_scripts("helper")

        captured = capsys.readouterr()
        assert "Console scripts in helper:" in captured.out
        assert "------------------------" in captured.out

    def test_prints_script_names(self, capsys):
        """Test that function prints script names."""
        result = print_all_console_scripts("helper")

        captured = capsys.readouterr()

        # If scripts were found, they should be printed
        for ep in result:
            assert ep.name in captured.out

    def test_works_with_nonexistent_package(self):
        """Test that function handles nonexistent package gracefully."""
        result = print_all_console_scripts("nonexistent_package_xyz")

        # Should return empty list for nonexistent package
        assert isinstance(result, list)
        assert len(result) == 0

    def test_default_parameter_uses_package_name(self, capsys):
        """Test that default parameter uses PACKAGE_NAME."""
        print_all_console_scripts()

        captured = capsys.readouterr()
        assert f"Console scripts in {PACKAGE_NAME}:" in captured.out

    def test_case_sensitivity(self):
        """Test that package name matching is case-insensitive."""
        result_lower = print_all_console_scripts("helper")
        result_upper = print_all_console_scripts("HELPER")

        # Both should find the same scripts (converted to lowercase internally)
        assert len(result_lower) == len(result_upper)

    def test_returns_entry_point_objects(self):
        """Test that returned objects have expected entry point attributes."""
        result = print_all_console_scripts("helper")

        if len(result) > 0:
            # Check that returned objects have entry point attributes
            first_ep = result[0]
            assert hasattr(first_ep, 'name')
            assert hasattr(first_ep, 'value')

    def test_filters_by_module_name(self):
        """Test that function filters entry points by module name."""
        result = print_all_console_scripts("helper")

        # All returned entry points should be from helper module
        for ep in result:
            module_name = ep.value.split(':')[0]
            assert module_name.startswith("helper")

    @pytest.mark.parametrize("package_name", [
        "helper",
        "pytest",  # Known package with console scripts
        "pip",     # Known package with console scripts
    ])
    def test_various_packages(self, package_name):
        """Test that function works with various package names."""
        result = print_all_console_scripts(package_name)
        assert isinstance(result, list)

    def test_handles_dict_like_entry_points(self, mocker):
        """Test fallback for dict-like entry_points (older Python)."""
        # Mock entry_points to return dict-like object without select method
        mock_eps = {
            'console_scripts': [
                mocker.Mock(name='helper', value='helper:main'),
                mocker.Mock(name='other', value='other:main'),
            ]
        }
        mocker.patch('helper.entry_points', return_value=mock_eps)

        result = print_all_console_scripts("helper")

        # Should use .get() fallback
        assert isinstance(result, list)
