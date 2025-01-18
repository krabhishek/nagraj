"""Tests for the 'add-domain' command."""

from pathlib import Path

from click.testing import CliRunner

from nagraj.cli.main import cli


def test_add_domain_creates_structure(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'add-domain' command creates the expected structure."""
    domain_name = "test-domain"
    result = cli_runner.invoke(
        cli,
        ["add-domain", domain_name, "-p", str(sample_project)],
    )
    assert result.exit_code == 0

    # Check domain directory structure
    domain_dir = sample_project / "src" / "domains" / domain_name
    assert domain_dir.is_dir()
    assert (domain_dir / "__init__.py").is_file()

    # Check base directory and files
    base_dir = domain_dir / "base"
    assert base_dir.is_dir()
    assert (base_dir / "__init__.py").is_file()

    # Check base class files exist and have correct content
    base_files = {
        "base_test_domain_entity.py": ("BaseTestDomainEntity", "entity"),
        "base_test_domain_value_object.py": (
            "BaseTestDomainValueObject",
            "value object",
        ),
        "base_test_domain_aggregate_root.py": (
            "BaseTestDomainAggregateRoot",
            "aggregate root",
        ),
        "base_test_domain_domain_event.py": (
            "BaseTestDomainDomainEvent",
            "domain event",
        ),
    }
    for file_name, (class_name, base_type) in base_files.items():
        file_path = base_dir / file_name
        assert file_path.is_file()
        content = file_path.read_text()

        # Check imports
        assert "from src.shared.base" in content

        # Check class names
        assert f"class {class_name}(" in content

        # Check docstrings
        assert f'"""Base {base_type} for {domain_name} domain."""' in content


def test_add_domain_with_dash_creates_correct_files(
    cli_runner: CliRunner, sample_project: Path
) -> None:
    """Test that 'add-domain' command creates correctly named files for domains with dashes."""
    domain_name = "order-management"
    result = cli_runner.invoke(
        cli,
        ["add-domain", domain_name, "-p", str(sample_project)],
    )
    assert result.exit_code == 0

    # Check base class files exist and have correct content
    base_dir = sample_project / "src" / "domains" / domain_name / "base"
    assert base_dir.is_dir()

    # Check one of the base class files
    entity_file = base_dir / "base_order_management_entity.py"
    assert entity_file.is_file()
    content = entity_file.read_text()

    # Check class name uses PascalCase
    assert "class BaseOrderManagementEntity(" in content
    assert "from src.shared.base.base_entity import BaseEntity" in content
    assert '"""Base entity for order-management domain."""' in content


def test_add_domain_updates_config(cli_runner: CliRunner, sample_project: Path) -> None:
    """Test that 'add-domain' command updates project configuration."""
    domain_name = "test-domain"
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
        ["add-domain", "test-domain", "-p", str(temp_project_dir / "nonexistent")],
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
