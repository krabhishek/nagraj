"""Tests for the 'add-domain' command."""

from pathlib import Path

from click.testing import CliRunner

from nagraj.cli.main import cli


def test_add_domain_creates_structure(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'add-domain' command creates the expected structure."""
    domain_name = "test_domain"
    result = cli_runner.invoke(
        cli,
        ["add-domain", domain_name, "-p", str(sample_project)],
    )
    assert result.exit_code == 0

    # Check domain directory structure
    domain_dir = sample_project / "src" / "domains" / domain_name
    assert domain_dir.is_dir()
    assert (domain_dir / "__init__.py").is_file()


def test_add_domain_updates_config(cli_runner: CliRunner, sample_project: Path) -> None:
    """Test that 'add-domain' command updates project configuration."""
    domain_name = "test_domain"
    result = cli_runner.invoke(
        cli,
        ["add-domain", domain_name, "-p", str(sample_project)],
    )
    assert result.exit_code == 0

    # Check if domain is in config
    config_file = sample_project / ".nagraj.yaml"
    content = config_file.read_text()
    assert domain_name in content


def test_add_domain_fails_on_nonexistent_project(
    cli_runner: CliRunner, temp_project_dir: Path
) -> None:
    """Test that 'add-domain' command fails if project doesn't exist."""
    result = cli_runner.invoke(
        cli,
        ["add-domain", "test_domain", "-p", str(temp_project_dir / "nonexistent")],
    )
    assert result.exit_code != 0
    assert "not a nagraj project" in result.output.lower()


def test_add_domain_fails_on_duplicate(
    cli_runner: CliRunner, sample_project_with_domain: tuple[Path, str]
) -> None:
    """Test that 'add-domain' command fails if domain already exists."""
    project_path, domain_name = sample_project_with_domain
    result = cli_runner.invoke(
        cli,
        ["add-domain", domain_name, "-p", str(project_path)],
    )
    assert result.exit_code != 0
    assert "already exists" in result.output.lower()
