"""Tests for the configuration schema."""

import pytest

from nagraj.config.schema import (
    BoundedContextConfig,
    DomainConfig,
    DomainType,
    NagrajProjectConfig,
)


def test_domain_type_values() -> None:
    """Test that DomainType enum has expected values."""
    assert DomainType.CORE == "core"
    assert DomainType.SUPPORTING == "supporting"
    assert DomainType.GENERIC == "generic"


def test_bounded_context_config_defaults() -> None:
    """Test BoundedContextConfig default values."""
    context = BoundedContextConfig(name="test_context")
    assert context.name == "test_context"
    assert context.has_api is True
    assert context.has_persistence is True
    assert context.dependencies == []


def test_domain_config_defaults() -> None:
    """Test DomainConfig default values."""
    domain = DomainConfig(name="test_domain")
    assert domain.name == "test_domain"
    assert domain.type == DomainType.CORE
    assert domain.bounded_contexts == {}


def test_project_config_validation(sample_config: NagrajProjectConfig) -> None:
    """Test project configuration validation."""
    errors = sample_config.validate_structure("nonexistent")
    assert len(errors) > 0
    print("\nActual errors:", errors)  # Debug output
    assert any("missing required directory" in error.lower() for error in errors)


def test_project_config_add_domain(sample_config: NagrajProjectConfig) -> None:
    """Test adding domain to project configuration."""
    domain = DomainConfig(name="test_domain")
    sample_config.add_domain(domain)
    assert "test_domain" in sample_config.domains
    assert sample_config.domains["test_domain"].type == DomainType.CORE


def test_project_config_add_bounded_context(sample_config: NagrajProjectConfig) -> None:
    """Test adding bounded context to project configuration."""
    # Add domain first
    domain = DomainConfig(name="test_domain")
    sample_config.add_domain(domain)

    # Add bounded context
    context = BoundedContextConfig(name="test_context")
    sample_config.add_bounded_context("test_domain", context)

    assert "test_context" in sample_config.domains["test_domain"].bounded_contexts


def test_project_config_add_bounded_context_fails_on_nonexistent_domain(
    sample_config: NagrajProjectConfig,
) -> None:
    """Test that adding bounded context to nonexistent domain fails."""
    context = BoundedContextConfig(name="test_context")
    with pytest.raises(ValueError, match="does not exist"):
        sample_config.add_bounded_context("nonexistent", context)
