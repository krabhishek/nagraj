"""Tests for bounded context-related commands."""

from pathlib import Path

from click.testing import CliRunner

from nagraj.cli.main import cli


def test_add_bounded_context_creates_structure(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'add bc' command creates the expected structure."""
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

    # Check bounded context directory structure
    context_dir = sample_project / "src" / "domains" / domain_name / context_name
    assert context_dir.is_dir()
    assert (context_dir / "__init__.py").is_file()

    # Check domain layer directories
    domain_dir = context_dir / "domain"
    assert domain_dir.is_dir()
    assert (domain_dir / "__init__.py").is_file()
    assert (domain_dir / "entities").is_dir()
    assert (domain_dir / "value_objects").is_dir()
    assert (domain_dir / "events").is_dir()

    # Check application layer directories
    app_dir = context_dir / "application"
    assert app_dir.is_dir()
    assert (app_dir / "__init__.py").is_file()
    assert (app_dir / "commands").is_dir()
    assert (app_dir / "queries").is_dir()
    assert (app_dir / "handlers").is_dir()

    # Check infrastructure layer directories
    infra_dir = context_dir / "infrastructure"
    assert infra_dir.is_dir()
    assert (infra_dir / "__init__.py").is_file()
    assert (infra_dir / "repositories").is_dir()
    assert (infra_dir / "migrations").is_dir()

    # Check presentation layer directories
    presentation_dir = context_dir / "presentation"
    assert presentation_dir.is_dir()
    assert (presentation_dir / "__init__.py").is_file()
    assert (presentation_dir / "controllers").is_dir()
    assert (presentation_dir / "schemas").is_dir()


def test_add_bounded_context_updates_config(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'add bc' command updates project configuration."""
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

    # Check config file
    config_path = sample_project / ".nagraj.yaml"
    assert config_path.is_file()

    # Check bounded context in config
    import yaml

    config = yaml.safe_load(config_path.read_text())
    assert context_name in config["domains"][domain_name]["bounded_contexts"]


def test_add_bounded_context_fails_on_nonexistent_domain(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'add bc' command fails when domain does not exist."""
    result = cli_runner.invoke(
        cli,
        [
            "add",
            "bc",
            "nonexistent-domain",
            "test-context",
            "--project-dir",
            str(sample_project),
        ],
    )
    assert result.exit_code != 0
    assert "domain does not exist" in result.output.lower()


def test_add_bounded_context_fails_on_duplicate(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'add bc' command fails when bounded context already exists."""
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

    # Try to add it again
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
    assert result.exit_code != 0
    assert "already exists" in result.output.lower()
