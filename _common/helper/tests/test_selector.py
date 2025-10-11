"""Test cases for selector module."""
import pytest
from helper.selector import prompt_multi_selection, prompt_single_selection


class TestPromptSingleSelection:
    """Test suite for prompt_single_selection function."""

    def test_raises_value_error_for_empty_options(self):
        """Test that ValueError is raised when options list is empty."""
        with pytest.raises(ValueError, match="No options retrieved for selection"):
            prompt_single_selection("test", [])

    def test_raises_value_error_for_none_options(self):
        """Test that ValueError is raised when options is None."""
        with pytest.raises(ValueError, match="No options retrieved for selection"):
            prompt_single_selection("test", None)

    def test_returns_selected_option(self, mocker):
        """Test that selected option is returned."""
        mock_inquirer = mocker.patch("helper.selector.inquirer")
        mock_select = mocker.Mock()
        mock_select.execute.return_value = "option2"
        mock_inquirer.select.return_value = mock_select

        options = ["option1", "option2", "option3"]
        result = prompt_single_selection("test", options)

        assert result == "option2"
        mock_inquirer.select.assert_called_once_with(
            message="Please choose the test",
            choices=options,
            default=None,
        )

    def test_uses_custom_message(self, mocker):
        """Test that custom message is used when provided."""
        mock_inquirer = mocker.patch("helper.selector.inquirer")
        mock_select = mocker.Mock()
        mock_select.execute.return_value = "A"
        mock_inquirer.select.return_value = mock_select

        result = prompt_single_selection("test", ["A", "B"], message="Custom message")

        mock_inquirer.select.assert_called_once_with(
            message="Custom message",
            choices=["A", "B"],
            default=None,
        )

    def test_handles_various_option_types(self, mocker):
        """Test that various option types are handled."""
        mock_inquirer = mocker.patch("helper.selector.inquirer")
        mock_select = mocker.Mock()
        mock_select.execute.return_value = 42
        mock_inquirer.select.return_value = mock_select

        # Test with integer options
        options = [1, 2, 3, 42]
        result = prompt_single_selection("number", options)
        assert result == 42

    @pytest.mark.parametrize("options,expected_calls", [
        (["A"], 1),
        (["A", "B", "C", "D"], 1),
        (list(range(100)), 1),
    ])
    def test_called_once_regardless_of_option_count(self, mocker, options, expected_calls):
        """Test that select is called once regardless of option count."""
        mock_inquirer = mocker.patch("helper.selector.inquirer")
        mock_select = mocker.Mock()
        mock_select.execute.return_value = options[0]
        mock_inquirer.select.return_value = mock_select

        prompt_single_selection("test", options)

        assert mock_inquirer.select.call_count == expected_calls


class TestPromptMultiSelection:
    """Test suite for prompt_multi_selection function."""

    def test_raises_value_error_for_empty_options(self):
        """Test that ValueError is raised when options list is empty."""
        with pytest.raises(ValueError, match="No options retrieved for selection"):
            prompt_multi_selection("test", [], [])

    def test_raises_value_error_for_none_options(self):
        """Test that ValueError is raised when options is None."""
        with pytest.raises(ValueError, match="No options retrieved for selection"):
            prompt_multi_selection("test", None, [])

    def test_returns_selected_options(self, mocker):
        """Test that selected options are returned."""
        mock_inquirer = mocker.patch("helper.selector.inquirer")
        mock_checkbox = mocker.Mock()
        mock_checkbox.execute.return_value = ["B", "C"]
        mock_inquirer.checkbox.return_value = mock_checkbox

        options = ["A", "B", "C", "D"]
        pre_selected = ["B"]
        result = prompt_multi_selection("test", options, pre_selected)

        assert result == ["B", "C"]

    def test_uses_pre_selected_options(self, mocker):
        """Test that pre-selected options are marked as enabled."""
        mock_choice_class = mocker.patch("helper.selector.Choice")
        mock_inquirer = mocker.patch("helper.selector.inquirer")
        mock_checkbox = mocker.Mock()
        mock_checkbox.execute.return_value = ["B"]
        mock_inquirer.checkbox.return_value = mock_checkbox

        options = ["A", "B", "C"]
        pre_selected = ["B"]
        prompt_multi_selection("test", options, pre_selected)

        # Verify Choice was called for each option
        assert mock_choice_class.call_count == len(options)
        # Verify "B" was marked as enabled
        calls = mock_choice_class.call_args_list
        for call in calls:
            option = call[0][0]
            enabled = call[1]["enabled"]
            if option == "B":
                assert enabled is True
            else:
                assert enabled is False

    def test_uses_custom_message(self, mocker):
        """Test that custom message is used when provided."""
        mock_inquirer = mocker.patch("helper.selector.inquirer")
        mock_checkbox = mocker.Mock()
        mock_checkbox.execute.return_value = []
        mock_inquirer.checkbox.return_value = mock_checkbox

        prompt_multi_selection("test", ["A", "B"], [], message="Custom message")

        call_kwargs = mock_inquirer.checkbox.call_args[1]
        assert call_kwargs["message"] == "Custom message"

    def test_checkbox_has_cycle_enabled(self, mocker):
        """Test that checkbox has cycle enabled."""
        mock_inquirer = mocker.patch("helper.selector.inquirer")
        mock_checkbox = mocker.Mock()
        mock_checkbox.execute.return_value = []
        mock_inquirer.checkbox.return_value = mock_checkbox

        prompt_multi_selection("test", ["A", "B"], [])

        call_kwargs = mock_inquirer.checkbox.call_args[1]
        assert call_kwargs["cycle"] is True

    def test_transformer_function_works(self, mocker):
        """Test that transformer function is properly set."""
        mock_inquirer = mocker.patch("helper.selector.inquirer")
        mock_checkbox = mocker.Mock()
        mock_checkbox.execute.return_value = ["A", "B"]
        mock_inquirer.checkbox.return_value = mock_checkbox

        prompt_multi_selection("items", ["A", "B", "C"], [])

        call_kwargs = mock_inquirer.checkbox.call_args[1]
        transformer = call_kwargs["transformer"]

        # Test the transformer function
        result = transformer(["A", "B"])
        assert result == "2 items selected"

    def test_handles_empty_pre_selected_list(self, mocker):
        """Test that empty pre-selected list is handled."""
        mocker.patch("helper.selector.Choice")
        mock_inquirer = mocker.patch("helper.selector.inquirer")
        mock_checkbox = mocker.Mock()
        mock_checkbox.execute.return_value = []
        mock_inquirer.checkbox.return_value = mock_checkbox

        result = prompt_multi_selection("test", ["A", "B", "C"], [])

        assert result == []

    @pytest.mark.parametrize("options,pre_selected", [
        (["A", "B", "C"], ["A"]),
        (["A", "B", "C"], ["A", "C"]),
        (["A", "B", "C"], []),
        (list(range(10)), [0, 5, 9]),
    ])
    def test_various_option_combinations(self, mocker, options, pre_selected):
        """Test various combinations of options and pre-selected items."""
        mocker.patch("helper.selector.Choice")
        mock_inquirer = mocker.patch("helper.selector.inquirer")
        mock_checkbox = mocker.Mock()
        mock_checkbox.execute.return_value = pre_selected
        mock_inquirer.checkbox.return_value = mock_checkbox

        result = prompt_multi_selection("test", options, pre_selected)

        assert result == pre_selected

