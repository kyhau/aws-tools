"""Test cases for docker module."""
import logging

import pytest
from click.testing import CliRunner
from helper.docker import find_dangling_images, find_non_running_containers


class TestFindNonRunningContainers:
    """Test suite for find_non_running_containers function."""

    def test_finds_and_lists_exited_containers(self, mocker, caplog):
        """Test that exited containers are found and listed."""
        runner = CliRunner()

        # Mock Docker client and containers
        mock_container1 = mocker.Mock()
        mock_container1.short_id = "abc123"
        mock_container1.status = "exited"
        mock_container1.image.tags = ["nginx:latest"]

        mock_container2 = mocker.Mock()
        mock_container2.short_id = "def456"
        mock_container2.status = "exited"
        mock_container2.image.tags = ["redis:6.0"]

        mock_client = mocker.Mock()
        mock_client.containers.list.return_value = [mock_container1, mock_container2]

        # Mock docker.from_env()
        mocker.patch("helper.docker.client", mock_client)

        with caplog.at_level(logging.INFO):
            result = runner.invoke(find_non_running_containers)

        assert result.exit_code == 0
        assert "Found 2 non-running containers" in caplog.text
        mock_client.containers.list.assert_called_once_with(filters={"status": "exited"})

    def test_no_containers_found(self, mocker, caplog):
        """Test when no exited containers exist."""
        runner = CliRunner()

        mock_client = mocker.Mock()
        mock_client.containers.list.return_value = []

        mocker.patch("helper.docker.client", mock_client)

        with caplog.at_level(logging.INFO):
            result = runner.invoke(find_non_running_containers)

        assert result.exit_code == 0
        assert "Found 0 non-running containers" in caplog.text

    def test_removes_containers_with_flag(self, mocker, caplog):
        """Test that containers are removed when --remove flag is used."""
        runner = CliRunner()

        mock_container = mocker.Mock()
        mock_container.short_id = "abc123"
        mock_container.status = "exited"
        mock_container.image.tags = ["nginx:latest"]

        mock_client = mocker.Mock()
        mock_client.containers.list.return_value = [mock_container]

        mocker.patch("helper.docker.client", mock_client)

        with caplog.at_level(logging.INFO):
            result = runner.invoke(find_non_running_containers, ["--remove"])

        assert result.exit_code == 0
        mock_container.remove.assert_called_once()
        assert "Removed non-running images" in caplog.text

    def test_handles_removal_errors_gracefully(self, mocker):
        """Test that removal errors are caught and logged."""
        runner = CliRunner()

        mock_container = mocker.Mock()
        mock_container.short_id = "abc123"
        mock_container.status = "exited"
        mock_container.image.tags = ["nginx:latest"]
        mock_container.remove.side_effect = Exception("Permission denied")

        mock_client = mocker.Mock()
        mock_client.containers.list.return_value = [mock_container]

        mocker.patch("helper.docker.client", mock_client)

        result = runner.invoke(find_non_running_containers, ["--remove"])

        # Should not crash, error should be logged
        assert result.exit_code == 0
        mock_container.remove.assert_called_once()

    def test_short_flag_works(self, mocker):
        """Test that -r short flag works for removal."""
        runner = CliRunner()

        mock_container = mocker.Mock()
        mock_container.short_id = "abc123"
        mock_container.status = "exited"
        mock_container.image.tags = ["test:latest"]

        mock_client = mocker.Mock()
        mock_client.containers.list.return_value = [mock_container]

        mocker.patch("helper.docker.client", mock_client)

        result = runner.invoke(find_non_running_containers, ["-r"])

        assert result.exit_code == 0
        mock_container.remove.assert_called_once()


class TestFindDanglingImages:
    """Test suite for find_dangling_images function."""

    def test_finds_and_lists_dangling_images(self, mocker, caplog):
        """Test that dangling images are found and listed."""
        runner = CliRunner()

        mock_image1 = mocker.Mock()
        mock_image1.id = "sha256:abc123"
        mock_image1.tags = []

        mock_image2 = mocker.Mock()
        mock_image2.id = "sha256:def456"
        mock_image2.tags = []

        mock_client = mocker.Mock()
        mock_client.images.list.return_value = [mock_image1, mock_image2]

        mocker.patch("helper.docker.client", mock_client)

        with caplog.at_level(logging.INFO):
            result = runner.invoke(find_dangling_images)

        assert result.exit_code == 0
        assert "Found 2 dangling images" in caplog.text
        mock_client.images.list.assert_called_once_with(filters={"dangling": True})

    def test_no_dangling_images(self, mocker, caplog):
        """Test when no dangling images exist."""
        runner = CliRunner()

        mock_client = mocker.Mock()
        mock_client.images.list.return_value = []

        mocker.patch("helper.docker.client", mock_client)

        with caplog.at_level(logging.INFO):
            result = runner.invoke(find_dangling_images)

        assert result.exit_code == 0
        assert "Found 0 dangling images" in caplog.text

    def test_removes_dangling_images_with_flag(self, mocker, caplog):
        """Test that dangling images are pruned when --remove flag is used."""
        runner = CliRunner()

        mock_image = mocker.Mock()
        mock_image.id = "sha256:abc123"
        mock_image.tags = []

        mock_client = mocker.Mock()
        mock_client.images.list.return_value = [mock_image]

        mocker.patch("helper.docker.client", mock_client)

        with caplog.at_level(logging.INFO):
            result = runner.invoke(find_dangling_images, ["--remove"])

        assert result.exit_code == 0
        mock_client.images.prune.assert_called_once_with(filters={"dangling": True})
        assert "Removed dangling images" in caplog.text

    def test_short_flag_works_for_removal(self, mocker):
        """Test that -r short flag works for image removal."""
        runner = CliRunner()

        mock_image = mocker.Mock()
        mock_image.id = "sha256:abc123"
        mock_image.tags = []

        mock_client = mocker.Mock()
        mock_client.images.list.return_value = [mock_image]

        mocker.patch("helper.docker.client", mock_client)

        result = runner.invoke(find_dangling_images, ["-r"])

        assert result.exit_code == 0
        mock_client.images.prune.assert_called_once_with(filters={"dangling": True})

    def test_lists_image_details(self, mocker, caplog):
        """Test that image IDs and tags are displayed."""
        runner = CliRunner()

        mock_image = mocker.Mock()
        mock_image.id = "sha256:abc123def456"
        mock_image.tags = ["<none>:<none>"]

        mock_client = mocker.Mock()
        mock_client.images.list.return_value = [mock_image]

        mocker.patch("helper.docker.client", mock_client)

        with caplog.at_level(logging.INFO):
            result = runner.invoke(find_dangling_images)

        assert result.exit_code == 0
        assert "ID" in caplog.text
        assert "Tags" in caplog.text

