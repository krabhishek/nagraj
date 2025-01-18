"""Tests for the project manager."""

from pathlib import Path

import pytest

from nagraj.config.schema import DomainConfig
from nagraj.core.project import ProjectManager


def test_project_manager_load_config(
    project_manager: ProjectManager, sample_project: Path
) -> None:
    """Test loading project configuration."""
    project_manager.project_path = sample_project
    config = project_manager._load_config(sample_project)

    assert config.name == "test_project"
    assert config.base_classes is not None
    assert "entity" in config.base_classes


def test_project_manager_save_config(
    project_manager: ProjectManager, sample_project: Path
) -> None:
    """Test saving project configuration."""
    project_manager.project_path = sample_project
    project_manager.config = project_manager._load_config(sample_project)

    # Add a domain
    domain = DomainConfig(name="test_domain")
    project_manager.config.add_domain(domain)
    project_manager._save_config()

    # Reload and verify
    config = project_manager._load_config(sample_project)
    assert "test_domain" in config.domains


def test_project_manager_add_domain(
    project_manager: ProjectManager, sample_project: Path
) -> None:
    """Test adding a domain."""
    domain_path = project_manager.add_domain(sample_project, "test_domain")
    assert domain_path.exists()
    assert domain_path.is_dir()

    # Check if domain was added to config
    config = project_manager._load_config(sample_project)
    assert "test_domain" in config.domains


def test_project_manager_add_bounded_context(
    project_manager: ProjectManager, sample_project_with_domain: tuple[Path, str]
) -> None:
    """Test adding a bounded context."""
    project_path, domain_name = sample_project_with_domain
    context_path = project_manager.add_bounded_context(
        project_path, domain_name, "test_context"
    )
    assert context_path.exists()
    assert context_path.is_dir()

    # Check if bounded context was added to config
    config = project_manager._load_config(project_path)
    assert "test_context" in config.domains[domain_name].bounded_contexts


def test_project_manager_fails_on_duplicate_domain(
    project_manager: ProjectManager, sample_project_with_domain: tuple[Path, str]
) -> None:
    """Test that adding duplicate domain fails."""
    project_path, domain_name = sample_project_with_domain
    with pytest.raises(ValueError, match="already exists"):
        project_manager.add_domain(project_path, domain_name)


def test_project_manager_fails_on_duplicate_context(
    project_manager: ProjectManager, sample_project_with_domain: tuple[Path, str]
) -> None:
    """Test that adding duplicate bounded context fails."""
    project_path, domain_name = sample_project_with_domain

    # Add first context
    project_manager.add_bounded_context(project_path, domain_name, "test_context")

    # Try to add duplicate
    with pytest.raises(ValueError, match="already exists"):
        project_manager.add_bounded_context(project_path, domain_name, "test_context")
