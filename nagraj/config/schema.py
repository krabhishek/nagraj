"""Schema definitions for nagraj project configuration."""

from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from pydantic import BaseModel, Field


class DomainType(str, Enum):
    """Type of domain in DDD architecture."""

    CORE = "core"
    SUPPORTING = "supporting"
    GENERIC = "generic"

    def __str__(self) -> str:
        """Return string representation for YAML serialization."""
        return self.value


def setup_yaml_representers() -> None:
    """Set up custom YAML representers."""

    def represent_domain_type(dumper: yaml.SafeDumper, data: DomainType) -> yaml.Node:
        """Represent DomainType enum as a string."""
        return dumper.represent_str(str(data))

    yaml.add_representer(DomainType, represent_domain_type, Dumper=yaml.SafeDumper)


def validate_entity_name(name: str) -> tuple[bool, str]:
    """Validate entity name format.

    Args:
        name: The entity name to validate.

    Returns:
        A tuple of (is_valid, error_message).
    """
    if not name:
        return False, "Entity name cannot be empty"

    # Check for invalid characters
    if any(c for c in name if not c.isalnum() and c not in "-_"):
        return (
            False,
            "Entity name can only contain letters, numbers, dashes, and underscores",
        )

    # Check for spaces
    if " " in name:
        return False, "Entity name cannot contain spaces"

    # Check for consecutive dashes or underscores
    if "--" in name or "__" in name:
        return False, "Entity name cannot contain consecutive dashes or underscores"

    # Check for starting/ending with dash or underscore
    if name.startswith(("-", "_")) or name.endswith(("-", "_")):
        return False, "Entity name cannot start or end with a dash or underscore"

    # Check for plural form
    parts = name.split("-")
    for part in parts:
        subparts = part.split("_")
        for subpart in subparts:
            if subpart.endswith("s") and not subpart.endswith(
                "ss"
            ):  # Allow words like 'address'
                return False, "Entity name parts should be singular"

    return True, ""


class BoundedContextConfig(BaseModel):
    """Configuration for a bounded context."""

    name: str
    description: Optional[str] = None
    dependencies: List[str] = Field(default_factory=list)
    has_api: bool = True
    has_persistence: bool = True


class DomainConfig(BaseModel):
    """Configuration for a domain."""

    name: str
    type: DomainType = DomainType.CORE
    description: Optional[str] = None
    bounded_contexts: Dict[str, BoundedContextConfig] = Field(default_factory=dict)

    @classmethod
    def validate_domain_name(cls, name: str) -> tuple[bool, str]:
        """Validate domain name format.

        Args:
            name: The domain name to validate.

        Returns:
            A tuple of (is_valid, error_message).
        """
        if not name:
            return False, "Domain name cannot be empty"

        # Check for invalid characters
        if any(c for c in name if not c.isalnum() and c not in "-_"):
            return (
                False,
                "Domain name can only contain letters, numbers, dashes, and underscores",
            )

        # Check for spaces
        if " " in name:
            return False, "Domain name cannot contain spaces"

        # Check for consecutive dashes or underscores
        if "--" in name or "__" in name:
            return False, "Domain name cannot contain consecutive dashes or underscores"

        # Check for starting/ending with dash or underscore
        if name.startswith(("-", "_")) or name.endswith(("-", "_")):
            return False, "Domain name cannot start or end with a dash or underscore"

        # Check for plural form
        parts = name.split("-")
        for part in parts:
            subparts = part.split("_")
            for subpart in subparts:
                if subpart.endswith("s") and not subpart.endswith(
                    "ss"
                ):  # Allow words like 'address'
                    return False, "Domain name parts should be singular"

        return True, ""

    @property
    def pascal_case_name(self) -> str:
        """Convert domain name to PascalCase.

        Example:
            'order-management' -> 'OrderManagement'
            'order_management' -> 'OrderManagement'
        """
        # Split by both dash and underscore
        parts = []
        for part in self.name.split("-"):
            parts.extend(part.split("_"))
        return "".join(part.capitalize() for part in parts)

    def model_dump(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Override model_dump to handle enum serialization."""
        data = super().model_dump(*args, **kwargs)
        data["type"] = str(data["type"])
        return data

    def __init__(self, **data: Any) -> None:
        """Initialize domain config with validation."""
        if "name" in data:
            is_valid, error = self.validate_domain_name(data["name"])
            if not is_valid:
                raise ValueError(f"Invalid domain name: {error}")
        super().__init__(**data)

    def add_bounded_context(self, context: BoundedContextConfig) -> None:
        """Add a bounded context to the domain."""
        if context.name in self.bounded_contexts:
            raise ValueError(f"Bounded context {context.name} already exists")
        self.bounded_contexts[context.name] = context

    def remove_bounded_context(self, context_name: str) -> None:
        """Remove a bounded context from the domain."""
        if context_name not in self.bounded_contexts:
            raise ValueError(f"Bounded context {context_name} does not exist")
        del self.bounded_contexts[context_name]


class NagrajProjectConfig(BaseModel):
    """Configuration for a nagraj project."""

    version: str = "1.0"
    created_at: datetime
    updated_at: datetime
    name: str
    description: Optional[str] = None
    author: Optional[str] = None
    domains: Dict[str, DomainConfig] = Field(default_factory=dict)
    base_classes: Dict[str, str] = Field(default_factory=dict)

    def add_domain(self, domain: DomainConfig) -> None:
        """Add a domain to the project configuration."""
        self.domains[domain.name] = domain
        self.updated_at = datetime.now(UTC)

    def add_bounded_context(
        self, domain_name: str, context: BoundedContextConfig
    ) -> None:
        """Add a bounded context to a domain."""
        if domain_name not in self.domains:
            raise ValueError(f"Domain {domain_name} does not exist")

        self.domains[domain_name].bounded_contexts[context.name] = context
        self.updated_at = datetime.now(UTC)

    def remove_domain(self, domain_name: str) -> None:
        """Remove a domain from the project configuration."""
        if domain_name not in self.domains:
            raise ValueError(f"Domain {domain_name} does not exist")
        del self.domains[domain_name]
        self.updated_at = datetime.now(UTC)

    def remove_bounded_context(self, domain_name: str, context_name: str) -> None:
        """Remove a bounded context from a domain."""
        if domain_name not in self.domains:
            raise ValueError(f"Domain {domain_name} does not exist")
        self.domains[domain_name].bounded_contexts.pop(context_name)
        self.updated_at = datetime.now(UTC)

    def model_dump(self, *args: Any, **kwargs: Any) -> Dict[str, Any]:
        """Override model_dump to handle datetime serialization."""
        data = super().model_dump(*args, **kwargs)
        data["created_at"] = data["created_at"].isoformat()
        data["updated_at"] = data["updated_at"].isoformat()
        return data

    def validate_structure(self, project_path: str) -> List[str]:
        """Validate project structure against DDD standards.

        Args:
            project_path: Path to the project root directory.

        Returns:
            List of validation errors, empty if valid.
        """
        errors: List[str] = []
        root = Path(project_path)

        if not root.exists():
            errors.append(f"Missing required directory: {project_path}")
            return errors

        # Check basic project structure
        required_dirs = [
            "src",
            "src/shared",
            "src/shared/base",
            "src/domains",
        ]
        for dir_path in required_dirs:
            if not (root / dir_path).is_dir():
                errors.append(f"Missing required directory: {dir_path}")

        # Check base classes
        base_files = {
            "base_entity.py": "entity",
            "base_value_object.py": "value_object",
            "base_aggregate_root.py": "aggregate_root",
            "base_domain_event.py": "domain_event",
        }
        for file_name, class_type in base_files.items():
            base_file = root / "src" / "shared" / "base" / file_name
            if not base_file.is_file():
                errors.append(f"Missing required file: {file_name}")
            elif class_type in self.base_classes:
                # TODO: Add content validation to ensure base class matches configuration
                pass

        # Validate domains
        domains_dir = root / "src" / "domains"
        if domains_dir.is_dir():
            # Check configured domains exist
            for domain_name, domain_config in self.domains.items():
                domain_path = domains_dir / domain_name
                if not domain_path.is_dir():
                    errors.append(f"Missing required directory: domains/{domain_name}")
                else:
                    # Validate domain structure
                    errors.extend(
                        self._validate_domain_structure(domain_path, domain_config)
                    )

        return errors

    def _validate_domain_structure(
        self, domain_path: Path, domain_config: DomainConfig
    ) -> List[str]:
        """Validate the structure of a domain directory.

        Args:
            domain_path: Path to the domain directory.
            domain_config: Configuration for the domain.

        Returns:
            List of validation errors.
        """
        errors: List[str] = []

        # Check bounded contexts
        for context_name, context_config in domain_config.bounded_contexts.items():
            context_path = domain_path / context_name
            if not context_path.is_dir():
                errors.append(
                    f"Missing required directory: domains/{domain_config.name}/{context_name}"
                )
            else:
                # Check bounded context structure
                required_dirs = [
                    "domain/entities",
                    "domain/value_objects",
                    "application/commands",
                    "application/queries",
                ]

                # Add interface directories if has_api is True
                if context_config.has_api:
                    required_dirs.extend(
                        [
                            "interfaces/fastapi/routes",
                            "interfaces/fastapi/controllers",
                            "interfaces/fastapi/schemas",
                        ]
                    )

                # Add infrastructure directories if has_persistence is True
                if context_config.has_persistence:
                    required_dirs.extend(
                        [
                            "infrastructure/repositories",
                            "infrastructure/migrations",
                        ]
                    )

                for dir_path in required_dirs:
                    if not (context_path / dir_path).is_dir():
                        errors.append(
                            f"Missing required directory: domains/{domain_config.name}/{context_name}/{dir_path}"
                        )

        return errors


# Set up YAML representers
setup_yaml_representers()
