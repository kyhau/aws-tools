"""Test cases for http module."""
import pytest
from helper.http import HTTPS_OK_CODES, check_response


class TestHttpsOkCodes:
    """Test suite for HTTPS_OK_CODES constant."""

    def test_contains_standard_success_codes(self):
        """Test that HTTPS_OK_CODES contains standard HTTP success codes."""
        assert 200 in HTTPS_OK_CODES
        assert 201 in HTTPS_OK_CODES
        assert 202 in HTTPS_OK_CODES

    def test_has_three_codes(self):
        """Test that HTTPS_OK_CODES contains exactly three codes."""
        assert len(HTTPS_OK_CODES) == 3

    def test_all_codes_are_2xx(self):
        """Test that all codes are in the 2xx range."""
        for code in HTTPS_OK_CODES:
            assert 200 <= code < 300


class TestCheckResponse:
    """Test suite for check_response function."""

    def test_returns_true_for_200_status(self):
        """Test that 200 status code returns True."""
        response = {
            "ResponseMetadata": {
                "HTTPStatusCode": 200
            }
        }
        assert check_response(response) is True

    def test_returns_true_for_201_status(self):
        """Test that 201 status code returns True."""
        response = {
            "ResponseMetadata": {
                "HTTPStatusCode": 201
            }
        }
        assert check_response(response) is True

    def test_returns_true_for_202_status(self):
        """Test that 202 status code returns True."""
        response = {
            "ResponseMetadata": {
                "HTTPStatusCode": 202
            }
        }
        assert check_response(response) is True

    def test_returns_false_for_400_status(self):
        """Test that 400 status code returns False."""
        response = {
            "ResponseMetadata": {
                "HTTPStatusCode": 400
            }
        }
        assert check_response(response) is False

    def test_returns_false_for_500_status(self):
        """Test that 500 status code returns False."""
        response = {
            "ResponseMetadata": {
                "HTTPStatusCode": 500
            }
        }
        assert check_response(response) is False

    def test_returns_false_for_404_status(self):
        """Test that 404 status code returns False."""
        response = {
            "ResponseMetadata": {
                "HTTPStatusCode": 404
            }
        }
        assert check_response(response) is False

    def test_logs_error_for_non_ok_status(self, mocker, caplog):
        """Test that error is logged for non-OK status codes."""
        import logging

        response = {
            "ResponseMetadata": {
                "HTTPStatusCode": 500
            },
            "Error": {
                "Code": "InternalServerError",
                "Message": "Server error"
            }
        }

        with caplog.at_level(logging.ERROR):
            result = check_response(response)

        assert result is False
        assert "Response:" in caplog.text

    def test_does_not_log_for_ok_status(self, mocker, caplog):
        """Test that no error is logged for OK status codes."""
        import logging

        response = {
            "ResponseMetadata": {
                "HTTPStatusCode": 200
            }
        }

        with caplog.at_level(logging.ERROR):
            result = check_response(response)

        assert result is True
        # Should not have logged anything at ERROR level
        assert not caplog.text

    @pytest.mark.parametrize("status_code,expected", [
        (200, True),
        (201, True),
        (202, True),
        (199, False),
        (203, False),
        (300, False),
        (400, False),
        (401, False),
        (403, False),
        (404, False),
        (500, False),
        (502, False),
        (503, False),
    ])
    def test_various_status_codes(self, status_code, expected):
        """Test check_response with various HTTP status codes."""
        response = {
            "ResponseMetadata": {
                "HTTPStatusCode": status_code
            }
        }
        assert check_response(response) is expected

    def test_handles_complex_response_structure(self):
        """Test that complex response structures are handled correctly."""
        response = {
            "ResponseMetadata": {
                "HTTPStatusCode": 200,
                "RequestId": "abc-123",
                "HTTPHeaders": {
                    "content-type": "application/json"
                }
            },
            "Data": {
                "Key": "Value"
            }
        }
        assert check_response(response) is True

    def test_response_with_additional_metadata(self):
        """Test response with additional metadata fields."""
        response = {
            "ResponseMetadata": {
                "HTTPStatusCode": 201,
                "RetryAttempts": 0,
                "RequestId": "xyz-789"
            },
            "ResourceId": "resource-123"
        }
        assert check_response(response) is True
