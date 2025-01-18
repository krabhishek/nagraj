"""Tests for the 'add-bc' command."""

from pathlib import Path

from click.testing import CliRunner

from nagraj.cli.main import cli


def test_add_bounded_context_creates_structure(
    cli_runner: CliRunner, sample_project_with_domain: tuple[Path, str]
) -> None:
    """Test that 'add-bc' command creates the expected structure."""
    project_path, domain_name = sample_project_with_domain
    context_name = "test_context"

    result = cli_runner.invoke(
        cli,
        ["add-bc", domain_name, context_name, "-p", str(project_path)],
    )
    assert result.exit_code == 0

    # Check bounded context directory structure
    context_dir = project_path / "src" / "domains" / domain_name / context_name
    assert context_dir.is_dir()

    # Check DDD layers
    assert (context_dir / "domain" / "entities").is_dir()
    assert (context_dir / "domain" / "value_objects").is_dir()
    assert (context_dir / "application" / "commands").is_dir()
    assert (context_dir / "application" / "queries").is_dir()
    assert (context_dir / "interfaces" / "fastapi" / "routes").is_dir()
    assert (context_dir / "infrastructure" / "repositories").is_dir()


def test_add_bounded_context_updates_config(
    cli_runner: CliRunner, sample_project_with_domain: tuple[Path, str]
) -> None:
    """Test that 'add-bc' command updates project configuration."""
    project_path, domain_name = sample_project_with_domain
    context_name = "test_context"

    result = cli_runner.invoke(
        cli,
        ["add-bc", domain_name, context_name, "-p", str(project_path)],
    )
    assert result.exit_code == 0

    # Check if bounded context is in config
    config_file = project_path / ".nagraj.yaml"
    content = config_file.read_text()
    assert context_name in content


def test_add_bounded_context_fails_on_nonexistent_domain(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'add-bc' command fails if domain doesn't exist."""
    result = cli_runner.invoke(
        cli,
        ["add-bc", "nonexistent", "test_context", "-p", str(sample_project)],
    )
    assert result.exit_code != 0
    assert "does not exist" in result.output.lower()


def test_add_bounded_context_fails_on_duplicate(
    cli_runner: CliRunner, sample_project_with_domain: tuple[Path, str]
) -> None:
    """Test that 'add-bc' command fails if bounded context already exists."""
    project_path, domain_name = sample_project_with_domain
    context_name = "test_context"

    # Add first bounded context
    result = cli_runner.invoke(
        cli,
        ["add-bc", domain_name, context_name, "-p", str(project_path)],
    )
    assert result.exit_code == 0

    # Try to add duplicate
    result = cli_runner.invoke(
        cli,
        ["add-bc", domain_name, context_name, "-p", str(project_path)],
    )
    assert result.exit_code != 0
    assert "already exists" in result.output.lower()
