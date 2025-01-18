"""Tests for the 'remove' command group."""

from pathlib import Path

from click.testing import CliRunner

from nagraj.cli.main import cli


def test_remove_domain_removes_structure(
    cli_runner: CliRunner, sample_project_with_domain: tuple[Path, str]
) -> None:
    """Test that 'remove domain' command removes the domain structure."""
    project_path, domain_name = sample_project_with_domain

    result = cli_runner.invoke(
        cli,
        ["remove", "domain", domain_name, "-p", str(project_path)],
    )
    assert result.exit_code == 0

    # Check domain directory is removed
    domain_dir = project_path / "src" / "domains" / domain_name
    assert not domain_dir.exists()

    # Check domain is removed from config
    config_file = project_path / ".nagraj.yaml"
    content = config_file.read_text()
    assert domain_name not in content


def test_remove_domain_fails_on_nonexistent_project(
    cli_runner: CliRunner, temp_project_dir: Path
) -> None:
    """Test that 'remove domain' command fails if project doesn't exist."""
    result = cli_runner.invoke(
        cli,
        [
            "remove",
            "domain",
            "test-domain",
            "-p",
            str(temp_project_dir / "nonexistent"),
        ],
    )
    assert result.exit_code != 0
    assert (
        "directory" in result.output.lower()
        and "does not exist" in result.output.lower()
    )


def test_remove_domain_fails_on_nonexistent_domain(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'remove domain' command fails if domain doesn't exist."""
    result = cli_runner.invoke(
        cli,
        ["remove", "domain", "nonexistent", "-p", str(sample_project)],
    )
    assert result.exit_code != 0
    assert "does not exist" in result.output.lower()


def test_remove_bounded_context_removes_structure(
    cli_runner: CliRunner, sample_project_with_domain: tuple[Path, str]
) -> None:
    """Test that 'remove bc' command removes the bounded context structure."""
    project_path, domain_name = sample_project_with_domain
    context_name = "test-context"

    # First add a bounded context
    result = cli_runner.invoke(
        cli,
        ["add", "bc", domain_name, context_name, "-p", str(project_path)],
    )
    assert result.exit_code == 0

    # Then remove it
    result = cli_runner.invoke(
        cli,
        ["remove", "bc", domain_name, context_name, "-p", str(project_path)],
    )
    assert result.exit_code == 0

    # Check bounded context directory is removed
    context_dir = project_path / "src" / "domains" / domain_name / context_name
    assert not context_dir.exists()

    # Check bounded context is removed from config
    config_file = project_path / ".nagraj.yaml"
    content = config_file.read_text()
    assert context_name not in content


def test_remove_bounded_context_fails_on_nonexistent_domain(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'remove bc' command fails if domain doesn't exist."""
    result = cli_runner.invoke(
        cli,
        ["remove", "bc", "nonexistent", "test-context", "-p", str(sample_project)],
    )
    assert result.exit_code != 0
    assert "does not exist" in result.output.lower()


def test_remove_bounded_context_fails_on_nonexistent_context(
    cli_runner: CliRunner, sample_project_with_domain: tuple[Path, str]
) -> None:
    """Test that 'remove bc' command fails if bounded context doesn't exist."""
    project_path, domain_name = sample_project_with_domain
    result = cli_runner.invoke(
        cli,
        ["remove", "bc", domain_name, "nonexistent", "-p", str(project_path)],
    )
    assert result.exit_code != 0
    assert "does not exist" in result.output.lower()
