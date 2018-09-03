from click.testing import CliRunner

from arki.aws import cognito


def test_get_tokens_failed():
    args = [
        "-t", "invalid.user@example.com:1234",
    ]
    runner = CliRunner()
    result = runner.invoke(cognito.main, args)
    assert result.exit_code == 1

