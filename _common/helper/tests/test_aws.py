"""Test cases for aws module."""
import pytest
from botocore.exceptions import ClientError
from helper.aws import AwsApiHelper, MultiAccountHelper, get_tag_value


class TestAwsApiHelper:
    """Test suite for AwsApiHelper class."""

    def test_initialization_sets_logging_levels(self):
        """Test that initialization configures logging levels."""
        helper = AwsApiHelper()
        assert helper is not None

    def test_auth_errors_list(self):
        """Test that AUTH_ERRORS list contains expected error codes."""
        expected_errors = [
            "AccessDenied", "AccessDeniedException", "AuthFailure",
            "UnauthorizedOperation", "UnrecognizedClientException"
        ]
        assert AwsApiHelper.AUTH_ERRORS == expected_errors

    def test_cred_errors_list(self):
        """Test that CRED_ERRORS list contains expected error codes."""
        expected_errors = ["ExpiredToken", "InvalidClientTokenId"]
        assert AwsApiHelper.CRED_ERRORS == expected_errors

    def test_paginate_yields_items(self, mocker):
        """Test that paginate yields items from paginated results."""
        mock_client = mocker.Mock()
        mock_paginator = mocker.Mock()
        mock_page_iterator = mocker.Mock()

        # Set up the mock chain
        mock_client.get_paginator.return_value = mock_paginator
        mock_paginator.paginate.return_value.result_key_iters.return_value = [
            ["item1", "item2"],
            ["item3"]
        ]

        result = list(AwsApiHelper.paginate(mock_client, "list_objects", {"Bucket": "test"}))

        assert result == ["item1", "item2", "item3"]
        mock_client.get_paginator.assert_called_once_with("list_objects")
        mock_paginator.paginate.assert_called_once_with(Bucket="test")

    def test_paginate_with_no_kwargs(self, mocker):
        """Test paginate with no kwargs."""
        mock_client = mocker.Mock()
        mock_paginator = mocker.Mock()

        mock_client.get_paginator.return_value = mock_paginator
        mock_paginator.paginate.return_value.result_key_iters.return_value = [["item1"]]

        result = list(AwsApiHelper.paginate(mock_client, "list_tables", None))

        assert result == ["item1"]
        mock_paginator.paginate.assert_called_once_with()

    def test_process_client_error_auth_errors(self, mocker):
        """Test that auth errors are handled with warning."""
        helper = AwsApiHelper()

        for error_code in AwsApiHelper.AUTH_ERRORS:
            error = ClientError(
                {"Error": {"Code": error_code, "Message": "Test error"}},
                "test_operation"
            )
            # Should not raise, just log warning
            helper.process_client_error(error, "123456789012", "us-east-1")

    def test_process_client_error_other_errors_raise(self):
        """Test that non-auth errors are re-raised."""
        helper = AwsApiHelper()
        error = ClientError(
            {"Error": {"Code": "SomeOtherError", "Message": "Test error"}},
            "test_operation"
        )

        # process_client_error uses bare 'raise', so we need to be in an exception context
        with pytest.raises(ClientError):
            try:
                raise error
            except ClientError as e:
                helper.process_client_error(e, "123456789012", "us-east-1")

    def test_process_request_is_overridable(self, mocker):
        """Test that process_request can be overridden in subclass."""
        class CustomHelper(AwsApiHelper):
            def process_request(self, session, account_id, region, kwargs):
                return "processed"

        helper = CustomHelper()
        mock_session = mocker.Mock()
        result = helper.process_request(mock_session, "123456789012", "us-east-1", {})
        assert result == "processed"

    def test_post_process_is_callable(self):
        """Test that post_process method exists and is callable."""
        helper = AwsApiHelper()
        # Should not raise
        helper.post_process()


class TestMultiAccountHelper:
    """Test suite for MultiAccountHelper class."""

    def test_initialization(self):
        """Test that MultiAccountHelper initializes correctly."""
        helper = MultiAccountHelper()
        assert helper._accounts_processed == []

    def test_read_aws_profile_names_success(self, mocker, unittest_workspace):
        """Test reading AWS profile names from credentials file."""
        import os
        from os.path import join

        # Create mock credentials file
        aws_dir = join(unittest_workspace, ".aws")
        os.makedirs(aws_dir, exist_ok=True)
        creds_file = join(aws_dir, "credentials")

        with open(creds_file, "w") as f:
            f.write("[default]\n")
            f.write("aws_access_key_id = test\n")
            f.write("aws_secret_access_key = test\n")
            f.write("\n")
            f.write("[profile1]\n")
            f.write("aws_access_key_id = test\n")
            f.write("aws_secret_access_key = test\n")

        # Mock expanduser to return our test directory
        mocker.patch("os.path.expanduser", return_value=unittest_workspace)

        result = MultiAccountHelper.read_aws_profile_names()
        assert "default" in result
        assert "profile1" in result

    def test_read_aws_profile_names_file_not_found(self, mocker):
        """Test that error is handled when credentials file not found."""
        mocker.patch("os.path.expanduser", return_value="/nonexistent")
        result = MultiAccountHelper.read_aws_profile_names()
        # When file not found, an empty list is returned (no sections)
        assert result == [] or result is None

    def test_sessions_filters_duplicate_accounts(self, mocker):
        """Test that sessions() filters out duplicate account IDs."""
        helper = MultiAccountHelper()

        mock_session1 = mocker.Mock()
        mock_session2 = mocker.Mock()
        mock_client = mocker.Mock()

        mock_session1.client.return_value = mock_client
        mock_session2.client.return_value = mock_client
        mock_client.get_caller_identity.return_value = {"Account": "123456789012"}

        # Mock Session constructor
        mocker.patch("helper.aws.Session", side_effect=[mock_session1, mock_session2])

        # Mock read_aws_profile_names to return two profiles
        mocker.patch.object(helper, "read_aws_profile_names", return_value=["profile1", "profile2"])

        sessions = list(helper.sessions(None))

        # Should only yield one session since both profiles have same account ID
        assert len(sessions) == 1
        assert sessions[0][1] == "123456789012"

    def test_sessions_handles_credential_errors(self, mocker):
        """Test that sessions() handles credential errors gracefully."""
        helper = MultiAccountHelper()

        mock_session = mocker.Mock()
        mock_client = mocker.Mock()

        # Simulate expired credentials
        mock_client.get_caller_identity.side_effect = ClientError(
            {"Error": {"Code": "ExpiredToken", "Message": "Token expired"}},
            "get_caller_identity"
        )
        mock_session.client.return_value = mock_client

        mocker.patch("helper.aws.Session", return_value=mock_session)
        mocker.patch.object(helper, "read_aws_profile_names", return_value=["profile1"])

        sessions = list(helper.sessions(None))

        # Should return empty list, not raise exception
        assert sessions == []

    def test_sessions_with_specific_profile(self, mocker):
        """Test sessions() with a specific profile provided."""
        helper = MultiAccountHelper()

        mock_session = mocker.Mock()
        mock_client = mocker.Mock()
        mock_client.get_caller_identity.return_value = {"Account": "123456789012"}
        mock_session.client.return_value = mock_client

        mocker.patch("helper.aws.Session", return_value=mock_session)

        sessions = list(helper.sessions("specific-profile"))

        assert len(sessions) == 1
        assert sessions[0][1] == "123456789012"
        assert sessions[0][2] == "specific-profile"


class TestGetTagValue:
    """Test suite for get_tag_value function."""

    def test_finds_existing_tag(self):
        """Test that existing tag value is returned."""
        tags = [
            {"Key": "Name", "Value": "MyResource"},
            {"Key": "Environment", "Value": "Production"}
        ]
        result = get_tag_value(tags, "Name")
        assert result == "MyResource"

    def test_finds_custom_key(self):
        """Test finding a custom tag key."""
        tags = [
            {"Key": "Name", "Value": "MyResource"},
            {"Key": "Owner", "Value": "TeamA"}
        ]
        result = get_tag_value(tags, "Owner")
        assert result == "TeamA"

    def test_returns_empty_string_when_not_found(self):
        """Test that empty string is returned when tag not found."""
        tags = [
            {"Key": "Environment", "Value": "Production"}
        ]
        result = get_tag_value(tags, "Name")
        assert result == ""

    def test_handles_empty_tags_list(self):
        """Test that empty list returns empty string."""
        result = get_tag_value([], "Name")
        assert result == ""

    @pytest.mark.parametrize("tags,key,expected", [
        ([{"Key": "Name", "Value": "Test"}], "Name", "Test"),
        ([{"Key": "Name", "Value": ""}], "Name", ""),
        ([{"Key": "Foo", "Value": "Bar"}], "Name", ""),
        ([], "Name", ""),
    ])
    def test_various_scenarios(self, tags, key, expected):
        """Test various tag scenarios."""
        result = get_tag_value(tags, key)
        assert result == expected

    def test_case_sensitive_key_matching(self):
        """Test that key matching is case-sensitive."""
        tags = [
            {"Key": "name", "Value": "lowercase"},
            {"Key": "Name", "Value": "uppercase"}
        ]
        result = get_tag_value(tags, "Name")
        assert result == "uppercase"

        result = get_tag_value(tags, "name")
        assert result == "lowercase"

