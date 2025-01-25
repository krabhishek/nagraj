"""Unit tests for the init command."""

from pathlib import Path
from subprocess import CalledProcessError
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from nagraj.cli.commands.init import get_git_config_value, init


@pytest.fixture
def cli_runner():
    """Fixture for click CLI runner."""
    return CliRunner()


@pytest.fixture
def temp_dir(tmp_path):
    """Fixture for temporary directory."""
    return tmp_path


def test_get_git_config_value_success():
    """Test successful git config value retrieval."""
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.stdout = "John Doe\n"
        mock_run.return_value.check = True

        result = get_git_config_value("user.name")
        assert result == "John Doe"
        mock_run.assert_called_once_with(
            ["git", "config", "--global", "--get", "user.name"],
            capture_output=True,
            text=True,
            check=True,
        )


def test_get_git_config_value_failure():
    """Test git config value retrieval failure."""
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = CalledProcessError(1, "git config")
        result = get_git_config_value("user.name")
        assert result is None


def test_init_command_basic(cli_runner, temp_dir):
    """Test basic init command execution."""
    with patch("nagraj.cli.commands.init.cookiecutter") as mock_cookiecutter, \
         patch("pathlib.Path.exists") as mock_exists:
        
        # Ensure template directory exists
        mock_exists.return_value = True

        result = cli_runner.invoke(
            init,
            [
                "--project-name", "test_project",
                "--project-root-dir", str(temp_dir),
                "--project-author-name", "Test Author",
                "--project-author-email", "test@example.com",
            ],
        )
        
        assert result.exit_code == 0
        mock_cookiecutter.assert_called_once()
        call_kwargs = mock_cookiecutter.call_args[1]
        
        # Verify template directory path is passed as first argument
        template_dir = Path(mock_cookiecutter.call_args[0][0])
        assert template_dir.name == "nagraj-full-project-template"
        
        # Verify context variables
        assert call_kwargs["extra_context"] == {
            "project_name": "test_project",
            "author_name": "Test Author",
            "author_email": "test@example.com",
            "project_description": "A Python project generated using nagraj",
            "python_version": "3.12",
            "version": "0.1.0",
        }
        assert call_kwargs["no_input"] is True
        assert call_kwargs["output_dir"] == str(temp_dir)


def test_init_command_with_defaults(cli_runner, temp_dir):
    """Test init command with default values."""
    with patch("nagraj.cli.commands.init.cookiecutter") as mock_cookiecutter, \
         patch("nagraj.cli.commands.init.get_git_config_value") as mock_git, \
         patch("pathlib.Path.exists") as mock_exists:
        
        # Ensure template directory exists
        mock_exists.return_value = True
        
        mock_git.side_effect = lambda key: {
            "user.name": "Git User",
            "user.email": "git@example.com"
        }.get(key)

        result = cli_runner.invoke(
            init,
            ["--project-root-dir", str(temp_dir)],
        )
        
        assert result.exit_code == 0
        mock_cookiecutter.assert_called_once()
        call_kwargs = mock_cookiecutter.call_args[1]
        
        # Verify default values
        assert call_kwargs["extra_context"]["project_name"] == "my_app"
        assert call_kwargs["extra_context"]["author_name"] == "Git User"
        assert call_kwargs["extra_context"]["author_email"] == "git@example.com"
        assert call_kwargs["no_input"] is True
        assert call_kwargs["output_dir"] == str(temp_dir)


def test_init_command_template_not_found(cli_runner, temp_dir):
    """Test init command when template directory is not found."""
    with patch("pathlib.Path.exists") as mock_exists:
        mock_exists.return_value = False
        
        result = cli_runner.invoke(
            init,
            [
                "--project-name", "test_project",
                "--project-root-dir", str(temp_dir),
            ],
        )
        
        assert result.exit_code != 0
        assert "Template directory not found" in result.output


def test_init_command_cookiecutter_error(cli_runner, temp_dir):
    """Test init command when cookiecutter fails."""
    with patch("nagraj.cli.commands.init.cookiecutter") as mock_cookiecutter, \
         patch("pathlib.Path.exists") as mock_exists:
        
        # Ensure template directory exists
        mock_exists.return_value = True
        
        # Make cookiecutter raise an exception
        mock_cookiecutter.side_effect = Exception("Cookiecutter failed")
        
        result = cli_runner.invoke(
            init,
            [
                "--project-name", "test_project",
                "--project-root-dir", str(temp_dir),
            ],
        )
        
        assert result.exit_code != 0
        assert "Failed to create project" in str(result.output) 