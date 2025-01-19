"""Tests for remove commands."""

from pathlib import Path

from click.testing import CliRunner

from nagraj.cli.main import cli


def test_remove_domain_removes_structure(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'remove domain' command removes the domain structure."""
    # First, add a domain
    domain_name = "test-domain"
    result = cli_runner.invoke(
        cli,
        ["add", "domain", domain_name, "--project-dir", str(sample_project)],
    )
    assert result.exit_code == 0

    # Then remove it
    result = cli_runner.invoke(
        cli,
        ["remove", "domain", domain_name, "--project-dir", str(sample_project)],
    )
    assert result.exit_code == 0

    # Check domain directory is removed
    domain_dir = sample_project / "src" / "domains" / domain_name
    assert not domain_dir.exists()

    # Check domain is removed from config
    config_path = sample_project / ".nagraj.yaml"
    assert config_path.is_file()

    import yaml

    config = yaml.safe_load(config_path.read_text())
    assert domain_name not in config["domains"]


def test_remove_domain_fails_on_nonexistent_project(
    cli_runner: CliRunner, temp_project_dir: Path
) -> None:
    """Test that 'remove domain' command fails when project does not exist."""
    result = cli_runner.invoke(
        cli,
        [
            "remove",
            "domain",
            "test-domain",
            "--project-dir",
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
    """Test that 'remove domain' command fails when domain does not exist."""
    result = cli_runner.invoke(
        cli,
        [
            "remove",
            "domain",
            "nonexistent-domain",
            "--project-dir",
            str(sample_project),
        ],
    )
    assert result.exit_code != 0
    assert "domain does not exist" in result.output.lower()


def test_remove_bounded_context_removes_structure(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'remove bc' command removes the bounded context structure."""
    # First, add a domain
    domain_name = "test-domain"
    result = cli_runner.invoke(
        cli,
        ["add", "domain", domain_name, "--project-dir", str(sample_project)],
    )
    assert result.exit_code == 0

    # Then add a bounded context
    context_name = "test-context"
    result = cli_runner.invoke(
        cli,
        [
            "add",
            "bc",
            domain_name,
            context_name,
            "--project-dir",
            str(sample_project),
        ],
    )
    assert result.exit_code == 0

    # Then remove it
    result = cli_runner.invoke(
        cli,
        [
            "remove",
            "bc",
            domain_name,
            context_name,
            "--project-dir",
            str(sample_project),
        ],
    )
    assert result.exit_code == 0

    # Check bounded context directory is removed
    context_dir = sample_project / "src" / "domains" / domain_name / context_name
    assert not context_dir.exists()

    # Check bounded context is removed from config
    config_path = sample_project / ".nagraj.yaml"
    assert config_path.is_file()

    import yaml

    config = yaml.safe_load(config_path.read_text())
    assert context_name not in config["domains"][domain_name]["bounded_contexts"]


def test_remove_bounded_context_fails_on_nonexistent_domain(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'remove bc' command fails when domain does not exist."""
    result = cli_runner.invoke(
        cli,
        [
            "remove",
            "bc",
            "nonexistent-domain",
            "test-context",
            "--project-dir",
            str(sample_project),
        ],
    )
    assert result.exit_code != 0
    assert "domain does not exist" in result.output.lower()


def test_remove_bounded_context_fails_on_nonexistent_context(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'remove bc' command fails when bounded context does not exist."""
    # First, add a domain
    domain_name = "test-domain"
    result = cli_runner.invoke(
        cli,
        ["add", "domain", domain_name, "--project-dir", str(sample_project)],
    )
    assert result.exit_code == 0

    # Try to remove a nonexistent bounded context
    result = cli_runner.invoke(
        cli,
        [
            "remove",
            "bc",
            domain_name,
            "nonexistent-context",
            "--project-dir",
            str(sample_project),
        ],
    )
    assert result.exit_code != 0
    assert "does not exist in domain" in result.output.lower()
