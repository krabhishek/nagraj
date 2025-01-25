"""Unit tests for the main CLI."""

import pytest
from click.testing import CliRunner

from nagraj.cli.main import cli


@pytest.fixture
def cli_runner():
    """Fixture for click CLI runner."""
    return CliRunner()


def test_cli_help(cli_runner):
    """Test CLI help command."""
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "Options:" in result.output
    assert "--help" in result.output
    assert "--version" in result.output


def test_cli_version(cli_runner):
    """Test CLI version command."""
    result = cli_runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "cli, version" in result.output


def test_cli_no_args(cli_runner):
    """Test CLI with no arguments."""
    result = cli_runner.invoke(cli)
    assert result.exit_code == 0
    assert "Usage:" in result.output


def test_cli_unknown_command(cli_runner):
    """Test CLI with unknown command."""
    result = cli_runner.invoke(cli, ["unknown"])
    assert result.exit_code != 0
    assert "No such command" in result.output 