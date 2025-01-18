"""Schema definitions for nagraj project configuration."""

from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

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

    def model_dump(self, *args, **kwargs) -> Dict:
        """Override model_dump to handle enum serialization."""
        data = super().model_dump(*args, **kwargs)
        data["type"] = str(data["type"])
        return data


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

    def model_dump(self, *args, **kwargs) -> Dict:
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
