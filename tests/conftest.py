"""Test fixtures for nagraj."""

import shutil
from pathlib import Path
from typing import Generator

import pytest
from click.testing import CliRunner

from nagraj.cli.main import cli


@pytest.fixture
def cli_runner() -> CliRunner:
    """Create a Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def temp_project_dir(tmp_path: Path) -> Generator[Path, None, None]:
    """Create a temporary directory for project tests."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir(parents=True, exist_ok=True)
    yield project_dir
    shutil.rmtree(project_dir)


@pytest.fixture
def project_manager() -> None:
    """Create a project manager instance for testing."""
    pass


@pytest.fixture
def sample_project(cli_runner: CliRunner, temp_project_dir: Path) -> Path:
    """Create a sample project for testing."""
    result = cli_runner.invoke(
        cli,
        [
            "new",
            "test_project",
            "-o",
            str(temp_project_dir),
            "-a",
            "Test Author",
            "--debug",
        ],
        catch_exceptions=False,
    )
    if result.exit_code != 0:
        print(f"Debug output: {result.output}")
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
        ["add", "domain", domain_name, "-p", str(sample_project), "--debug"],
        catch_exceptions=False,
    )
    if result.exit_code != 0:
        print(f"Debug output: {result.output}")
    assert result.exit_code == 0
    return sample_project, domain_name


@pytest.fixture
def sample_config() -> dict:
    """Create a sample project configuration for testing."""
    return {
        "name": "test_project",
        "created_at": "2024-01-01T00:00:00+00:00",
        "updated_at": "2024-01-01T00:00:00+00:00",
        "author": "Test Author",
        "base_classes": {
            "entity": "BaseEntity",
            "value_object": "BaseValueObject",
            "aggregate_root": "BaseAggregateRoot",
            "domain_event": "BaseDomainEvent",
        },
    }
