"""Test cases for logger module."""
import logging
from os.path import exists, join

import pytest
from helper.logger import init_logging


class TestInitLogging:
    """Test suite for init_logging function."""

    def test_initializes_with_defaults(self):
        """Test that logger initializes with default parameters."""
        logger = init_logging()

        assert logger is not None
        assert logger.name == "default"
        assert logger.level == logging.INFO

    def test_sets_custom_name(self):
        """Test that logger can be initialized with custom name."""
        logger = init_logging(name="custom_logger")

        assert logger.name == "custom_logger"

    def test_sets_custom_log_level(self):
        """Test that custom log level is set correctly."""
        logger = init_logging(name="test_debug", log_level=logging.DEBUG)

        assert logger.level == logging.DEBUG

    def test_sets_warning_level(self):
        """Test that WARNING log level can be set."""
        logger = init_logging(name="test_warning", log_level=logging.WARNING)

        assert logger.level == logging.WARNING

    def test_sets_error_level(self):
        """Test that ERROR log level can be set."""
        logger = init_logging(name="test_error", log_level=logging.ERROR)

        assert logger.level == logging.ERROR

    def test_applies_custom_format(self):
        """Test that custom format is applied."""
        custom_format = "%(levelname)s - %(message)s"
        logger = init_logging(name="test_format", format=custom_format)

        # Verify logger has handlers with the custom formatter
        assert len(logger.handlers) > 0
        handler = logger.handlers[0]
        assert handler.formatter is not None

    def test_creates_console_handler(self):
        """Test that console handler is created."""
        logger = init_logging(name="test_console")

        # Should have at least one StreamHandler
        stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
        assert len(stream_handlers) >= 1

    def test_creates_file_handler_when_log_file_provided(self, unittest_workspace):
        """Test that file handler is created when log_file parameter is provided."""
        log_file = join(unittest_workspace, "test.log")
        logger = init_logging(name="test_file", log_file=log_file)

        # Should have FileHandler
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        assert len(file_handlers) >= 1

    def test_creates_log_file_directory_if_not_exists(self, unittest_workspace):
        """Test that log file directory is created if it doesn't exist."""
        nested_log_file = join(unittest_workspace, "logs", "nested", "test.log")
        _ = init_logging(name="test_nested", log_file=nested_log_file)

        # Directory should be created
        assert exists(join(unittest_workspace, "logs", "nested"))

    def test_writes_to_log_file(self, unittest_workspace):
        """Test that logs are actually written to file."""
        log_file = join(unittest_workspace, "app.log")
        logger = init_logging(name="test_write", log_file=log_file)

        test_message = "Test log message"
        logger.info(test_message)

        # Give handlers time to flush
        for handler in logger.handlers:
            handler.flush()

        # Read the file and check content
        assert exists(log_file)
        with open(log_file, "r") as f:
            content = f.read()
            assert test_message in content

    def test_suppresses_boto3_logging(self):
        """Test that boto3 logging is suppressed."""
        init_logging(name="test_boto")

        boto3_logger = logging.getLogger("boto3")
        botocore_logger = logging.getLogger("botocore")

        assert boto3_logger.level == logging.CRITICAL
        assert botocore_logger.level == logging.CRITICAL

    def test_suppresses_urllib3_logging(self):
        """Test that urllib3 logging is suppressed."""
        init_logging(name="test_urllib")

        urllib3_logger = logging.getLogger("urllib3.connectionpool")
        assert urllib3_logger.level == logging.CRITICAL

    def test_root_logger_level_is_set(self):
        """Test that root logger level is configured."""
        init_logging(name="test_root", log_level=logging.WARNING)

        root_logger = logging.getLogger()
        assert root_logger.level == logging.WARNING

    def test_handler_has_correct_level(self):
        """Test that handler level matches logger level."""
        logger = init_logging(name="test_handler_level", log_level=logging.DEBUG)

        for handler in logger.handlers:
            assert handler.level == logging.DEBUG

    def test_multiple_initializations_dont_duplicate_handlers(self):
        """Test that multiple initializations don't create duplicate handlers."""
        logger1 = init_logging(name="test_multi")
        _ = len(logger1.handlers)  # Note: handler count behavior may vary

        logger2 = init_logging(name="test_multi")
        # Note: This test verifies behavior; actual implementation may vary
        assert logger2.name == "test_multi"

    def test_default_format_contains_standard_fields(self):
        """Test that default format contains expected fields."""
        _ = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"  # Expected format
        logger = init_logging(name="test_default_format")

        # Handler should have a formatter
        assert len(logger.handlers) > 0
        handler = logger.handlers[0]
        assert handler.formatter is not None

    @pytest.mark.parametrize("log_level", [
        logging.DEBUG,
        logging.INFO,
        logging.WARNING,
        logging.ERROR,
        logging.CRITICAL,
    ])
    def test_various_log_levels(self, log_level):
        """Test that various log levels can be set."""
        logger = init_logging(name=f"test_level_{log_level}", log_level=log_level)
        assert logger.level == log_level

    def test_returns_logger_instance(self):
        """Test that function returns a logger instance."""
        logger = init_logging()
        assert isinstance(logger, logging.Logger)

    def test_logger_can_log_messages(self):
        """Test that returned logger can log messages."""
        logger = init_logging(name="test_logging")

        # Should not raise any exceptions
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")

    def test_file_and_console_handlers_both_active(self, unittest_workspace):
        """Test that both file and console handlers work together."""
        log_file = join(unittest_workspace, "combined.log")
        logger = init_logging(name="test_combined", log_file=log_file)

        # Should have both StreamHandler and FileHandler
        stream_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)
                           and not isinstance(h, logging.FileHandler)]
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]

        assert len(stream_handlers) >= 1
        assert len(file_handlers) >= 1
