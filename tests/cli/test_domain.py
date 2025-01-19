"""Tests for domain-related commands."""

from pathlib import Path

from click.testing import CliRunner

from nagraj.cli.main import cli


def test_add_domain_creates_structure(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'add domain' command creates the expected structure."""
    domain_name = "test-domain"
    result = cli_runner.invoke(
        cli,
        ["add", "domain", domain_name, "--project-dir", str(sample_project)],
    )
    assert result.exit_code == 0

    # Check domain directory structure
    domain_dir = sample_project / "src" / "domains" / domain_name
    assert domain_dir.is_dir()
    assert (domain_dir / "__init__.py").is_file()
    assert (domain_dir / "base").is_dir()

    # Check base class files
    base_files = {
        "base_test_domain_entity.py": "BaseTestDomainEntity",
        "base_test_domain_value_object.py": "BaseTestDomainValueObject",
        "base_test_domain_aggregate_root.py": "BaseTestDomainAggregateRoot",
        "base_test_domain_domain_event.py": "BaseTestDomainDomainEvent",
    }

    for file_name, class_name in base_files.items():
        file_path = domain_dir / "base" / file_name
        assert file_path.is_file()
        content = file_path.read_text()
        assert class_name in content


def test_add_domain_with_dash_creates_correct_files(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'add domain' command creates correctly named files for domains with dashes."""
    domain_name = "order-management"
    result = cli_runner.invoke(
        cli,
        ["add", "domain", domain_name, "--project-dir", str(sample_project)],
    )
    assert result.exit_code == 0

    # Check base class files
    base_files = {
        "base_order_management_entity.py": "BaseOrderManagementEntity",
        "base_order_management_value_object.py": "BaseOrderManagementValueObject",
        "base_order_management_aggregate_root.py": "BaseOrderManagementAggregateRoot",
        "base_order_management_domain_event.py": "BaseOrderManagementDomainEvent",
    }

    base_dir = sample_project / "src" / "domains" / domain_name / "base"
    for file_name, class_name in base_files.items():
        file_path = base_dir / file_name
        assert file_path.is_file()
        content = file_path.read_text()
        assert class_name in content


def test_add_domain_updates_config(cli_runner: CliRunner, sample_project: Path) -> None:
    """Test that 'add domain' command updates project configuration."""
    domain_name = "test-domain"
    result = cli_runner.invoke(
        cli,
        ["add", "domain", domain_name, "--project-dir", str(sample_project)],
    )
    assert result.exit_code == 0

    # Check config file
    config_path = sample_project / ".nagraj.yaml"
    assert config_path.is_file()

    # Check domain in config
    import yaml

    config = yaml.safe_load(config_path.read_text())
    assert domain_name in config["domains"]


def test_add_domain_fails_on_nonexistent_project(
    cli_runner: CliRunner, temp_project_dir: Path
) -> None:
    """Test that 'add domain' command fails when project does not exist."""
    result = cli_runner.invoke(
        cli,
        [
            "add",
            "domain",
            "test-domain",
            "--project-dir",
            str(temp_project_dir / "nonexistent"),
        ],
    )
    assert result.exit_code != 0
    assert "not a nagraj project" in result.output.lower()


def test_add_domain_fails_on_duplicate(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'add domain' command fails when domain already exists."""
    # First, add a domain
    result = cli_runner.invoke(
        cli,
        ["add", "domain", "test-domain", "--project-dir", str(sample_project)],
    )
    assert result.exit_code == 0

    # Try to add it again
    result = cli_runner.invoke(
        cli,
        ["add", "domain", "test-domain", "--project-dir", str(sample_project)],
    )
    assert result.exit_code != 0
    assert "already exists" in result.output.lower()
