"""Tests for the 'validate' command."""

import shutil
from pathlib import Path

from click.testing import CliRunner

from nagraj.cli.main import cli


def test_validate_passes_on_valid_project(
    cli_runner: CliRunner, sample_project_with_domain: tuple[Path, str]
) -> None:
    """Test that 'validate' command passes on a valid project structure."""
    project_path, _ = sample_project_with_domain
    result = cli_runner.invoke(cli, ["validate", "-p", str(project_path)])
    assert result.exit_code == 0
    assert "valid" in result.output.lower()


def test_validate_fails_on_missing_directory(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'validate' command fails when required directory is missing."""
    # Remove a required directory
    shutil.rmtree(sample_project / "src" / "shared" / "base")

    result = cli_runner.invoke(cli, ["validate", "-p", str(sample_project)])
    assert result.exit_code != 0
    assert "missing required directory" in result.output.lower()


def test_validate_fails_on_missing_base_class(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'validate' command fails when base class file is missing."""
    # Remove a base class file
    (sample_project / "src" / "shared" / "base" / "base_entity.py").unlink()

    result = cli_runner.invoke(cli, ["validate", "-p", str(sample_project)])
    assert result.exit_code != 0
    assert "missing required file" in result.output.lower()


def test_validate_fails_on_missing_domain(
    cli_runner: CliRunner, sample_project_with_domain: tuple[Path, str]
) -> None:
    """Test that 'validate' command fails when configured domain is missing."""
    project_path, domain_name = sample_project_with_domain
    # Remove domain directory
    shutil.rmtree(project_path / "src" / "domains" / domain_name)

    result = cli_runner.invoke(cli, ["validate", "-p", str(project_path)])
    assert result.exit_code != 0
    assert "missing required directory" in result.output.lower()


def test_validate_fails_on_nonexistent_project(
    cli_runner: CliRunner, temp_project_dir: Path
) -> None:
    """Test that 'validate' command fails on non-existent project."""
    result = cli_runner.invoke(
        cli,
        ["validate", "-p", str(temp_project_dir / "nonexistent")],
    )
    assert result.exit_code != 0
    assert "not a nagraj project" in result.output.lower()
