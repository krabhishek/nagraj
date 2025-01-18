"""Pytest configuration and shared fixtures."""

import shutil
from datetime import datetime, timezone
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
    return CliRunner()


@pytest.fixture
def temp_project_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary directory for project tests."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    yield project_dir
    # Cleanup
    if project_dir.exists():
        shutil.rmtree(project_dir)


@pytest.fixture
def project_manager(temp_project_dir: Path) -> ProjectManager:
    """Create a project manager instance for testing."""
    manager = ProjectManager()
    manager.project_path = temp_project_dir
    return manager


@pytest.fixture
def sample_project(cli_runner: CliRunner, temp_project_dir: Path) -> Path:
    """Create a sample project for testing."""
    result = cli_runner.invoke(
        cli,
        ["new", "test_project", "-o", str(temp_project_dir), "-a", "Test Author"],
    )
    assert result.exit_code == 0
    return temp_project_dir / "test_project"


@pytest.fixture
def sample_project_with_domain(
    cli_runner: CliRunner, sample_project: Path
) -> tuple[Path, str]:
    """Create a sample project with a domain for testing."""
    domain_name = "test_domain"
    result = cli_runner.invoke(
        cli,
        ["add-domain", domain_name, "-p", str(sample_project), "--debug"],
        catch_exceptions=False,
    )
    if result.exit_code != 0:
        print(f"Debug output: {result.output}")
    assert result.exit_code == 0
    return sample_project, domain_name


@pytest.fixture
def sample_config() -> NagrajProjectConfig:
    """Create a sample project configuration for testing."""
    test_time = datetime(2024, 1, 1, tzinfo=timezone.utc)
    return NagrajProjectConfig(
        name="test_project",
        created_at=test_time,
        updated_at=test_time,
        author="Test Author",
        description="Test Project",
        base_classes={
            "entity": "pydantic.BaseModel",
            "value_object": "pydantic.BaseModel",
            "aggregate_root": "pydantic.BaseModel",
            "orm": "sqlmodel.SQLModel",
        },
    )
