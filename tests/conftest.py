"""Test fixtures for nagraj."""

from datetime import UTC, datetime
from pathlib import Path
from typing import Generator

import pytest
from click.testing import CliRunner

from nagraj.cli.main import cli
from nagraj.config.schema import NagrajProjectConfig
from nagraj.core.project import ProjectManager


@pytest.fixture
def cli_runner() -> CliRunner:
    """Create a Click CLI test runner."""
    return CliRunner(mix_stderr=False)


@pytest.fixture
def temp_project_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary directory for project tests."""
    yield tmp_path


@pytest.fixture
def sample_project(cli_runner: CliRunner, temp_project_dir: Path) -> Path:
    """Create a sample project for testing."""
    project_dir = temp_project_dir / "test_project"
    result = cli_runner.invoke(
        cli,
        [
            "new",
            "test_project",
            "--output-dir",
            str(temp_project_dir),
            "--domain",
            "core",
            "--context",
            "main",
            "--author",
            "Test Author",
            "--debug",
        ],
        catch_exceptions=False,
    )
    print(f"\nOutput: {result.output}")
    print(f"Stderr: {result.stderr}")
    print(f"Exit code: {result.exit_code}")
    assert result.exit_code == 0
    assert project_dir.exists()
    return project_dir


@pytest.fixture
def sample_project_with_domain(
    cli_runner: CliRunner, sample_project: Path
) -> tuple[Path, str]:
    """Create a sample project with a test domain for testing."""
    domain_name = "test-domain"
    result = cli_runner.invoke(
        cli,
        [
            "add",
            "domain",
            domain_name,
            "--project-dir",
            str(sample_project),
        ],
    )
    assert result.exit_code == 0
    return sample_project, domain_name


@pytest.fixture
def sample_config() -> NagrajProjectConfig:
    """Create a sample project configuration for testing."""
    return NagrajProjectConfig(
        name="test_project",
        created_at=datetime(2024, 1, 1, tzinfo=UTC),
        updated_at=datetime(2024, 1, 1, tzinfo=UTC),
        author="Test Author",
        base_classes={
            "entity": "BaseEntity",
            "value_object": "BaseValueObject",
            "aggregate_root": "BaseAggregateRoot",
            "domain_event": "BaseDomainEvent",
            "command": "BaseCommand",
            "query": "BaseQuery",
            "command_handler": "BaseCommandHandler",
            "query_handler": "BaseQueryHandler",
        },
        domains={},
    )


@pytest.fixture
def project_manager(temp_project_dir: Path) -> Generator[ProjectManager, None, None]:
    """Create a project manager instance for testing."""
    project_dir = temp_project_dir / "test_project"
    manager = ProjectManager()
    manager.project_path = project_dir
    yield manager
