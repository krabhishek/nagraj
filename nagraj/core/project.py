"""Project management functionality."""

from datetime import UTC, datetime
from pathlib import Path
from typing import Dict, Optional, Union

import yaml
from rich.console import Console

from nagraj.config.schema import (
    BoundedContextConfig,
    DomainConfig,
    NagrajProjectConfig,
)
from nagraj.config.settings import ProjectConfig, settings
from nagraj.core.template import template_engine

console = Console()


class ProjectManager:
    """Manages project structure and modifications."""

    def __init__(self) -> None:
        self.config: Optional[NagrajProjectConfig] = None
        self.project_path: Optional[Path] = None

    def _load_config(self, project_path: Union[str, Path]) -> NagrajProjectConfig:
        """Load nagraj project configuration."""
        config_path = Path(project_path) / ".nagraj.yaml"
        if not config_path.exists():
            raise ValueError(f"Not a nagraj project: {project_path}")

        try:
            with config_path.open("r") as f:
                config_data = yaml.safe_load(f)
            return NagrajProjectConfig(**config_data)
        except Exception as e:
            raise ValueError(f"Failed to load project configuration: {e}")

    def _save_config(self) -> None:
        """Save nagraj project configuration."""
        if not self.config or not self.project_path:
            return

        config_path = Path(self.project_path) / ".nagraj.yaml"
        try:
            with config_path.open("w") as f:
                yaml.safe_dump(
                    self.config.model_dump(exclude_none=True),
                    f,
                    default_flow_style=False,
                    sort_keys=False,
                )
        except Exception as e:
            raise ValueError(f"Failed to save project configuration: {e}")

    def _ensure_project_structure(self, project_path: Path) -> None:
        """Ensure all required directories exist in the project."""
        required_dirs = [
            "src",
            "src/shared",
            "src/shared/base",
            "src/domains",
        ]

        for dir_path in required_dirs:
            try:
                (project_path / dir_path).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                raise ValueError(f"Failed to create directory {dir_path}: {e}")

    def create_project(
        self,
        name: str,
        output_dir: Union[str, Path],
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Path:
        """Create a new project with the DDD structure."""
        try:
            # Convert output_dir to Path and ensure it exists
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Check if project directory already exists
            project_path = output_dir / name
            if project_path.exists():
                raise ValueError(f"Project directory {project_path} already exists")

            # Create project configuration
            config = ProjectConfig(name=name, description=description, author=author)
            now = datetime.now(UTC).isoformat()

            # Prepare template context
            context = {
                "cookiecutter": {
                    "project_name": name,
                    "project_description": description
                    or f"A DDD/CQRS project named {name}",
                    "author": author or "Unknown",
                    "python_version": config.python_version,
                    "dependencies": config.dependencies,
                    "base_classes": {
                        "entity_base": settings.base_classes.entity_base,
                        "aggregate_root_base": settings.base_classes.aggregate_root_base,
                        "value_object_base": settings.base_classes.value_object_base,
                        "orm_base": settings.base_classes.orm_base,
                    },
                    "created_at": now,
                    "updated_at": now,
                }
            }

            # Create project from template
            console.print(f"Creating project [bold blue]{name}[/]...")
            try:
                project_path = template_engine.generate_project(
                    "project", output_dir, context
                )
                console.print(f"Template generated at [green]{project_path}[/]")
            except Exception as e:
                raise ValueError(f"Failed to generate project template: {e}")

            # Ensure all required directories exist
            try:
                self._ensure_project_structure(project_path)
                console.print("Project structure created")
            except Exception as e:
                raise ValueError(f"Failed to create project structure: {e}")

            # Create base class files if they don't exist
            base_dir = project_path / "src" / "shared" / "base"
            base_files = [
                "base_entity.py",
                "base_value_object.py",
                "base_aggregate_root.py",
                "base_domain_event.py",
                "__init__.py",
            ]
            try:
                for file_name in base_files:
                    file_path = base_dir / file_name
                    if not file_path.exists():
                        template_engine.write_template(
                            f"project/{{{{cookiecutter.project_name}}}}/src/shared/base/{file_name}",
                            file_path,
                            {
                                "cookiecutter": context["cookiecutter"]
                            },  # Pass the cookiecutter context
                        )
                console.print("Base class files created")
            except Exception as e:
                raise ValueError(f"Failed to create base class files: {e}")

            # Create __init__.py files
            init_files = [
                Path("src/__init__.py"),
                Path("src/shared/__init__.py"),
                Path("src/domains/__init__.py"),
            ]
            try:
                for file_path in init_files:
                    init_path = Path(project_path / file_path)
                    if not init_path.exists():
                        template_engine.write_template(
                            f"project/{{{{cookiecutter.project_name}}}}/{file_path}",
                            init_path,
                            {
                                "cookiecutter": context["cookiecutter"]
                            },  # Pass the cookiecutter context
                        )
                console.print("Init files created")
            except Exception as e:
                raise ValueError(f"Failed to create init files: {e}")

            # Load and validate the generated configuration
            try:
                self.project_path = project_path
                self.config = self._load_config(project_path)
                console.print("Project configuration loaded")
            except Exception as e:
                raise ValueError(f"Failed to load project configuration: {e}")

            console.print(f"Project created at [bold green]{project_path}[/]")
            return project_path

        except Exception as e:
            console.print(f"[red]Debug: {str(e)}[/]")
            raise ValueError(f"Failed to create project: {e}")

    def add_domain(
        self,
        project_path: Union[str, Path],
        domain_name: str,
        context: Optional[Dict] = None,
    ) -> Path:
        """Add a new domain to an existing project."""
        try:
            self.project_path = Path(project_path)
            if not self.project_path.exists():
                raise ValueError(f"Not a nagraj project: {project_path}")

            try:
                self.config = self._load_config(self.project_path)
            except ValueError as e:
                if "not a nagraj project" in str(e).lower():
                    raise
                raise ValueError(f"Failed to load project configuration: {e}")

            domain_path = self.project_path / "src" / "domains" / domain_name
            if domain_path.exists():
                raise ValueError(f"Domain {domain_name} already exists")

            # Create domain configuration
            domain_config = DomainConfig(
                name=domain_name, description=f"Domain for {domain_name}"
            )
            self.config.add_domain(domain_config)

            # Generate domain files
            context = context or {}
            domain_config = DomainConfig(
                name=domain_name
            )  # Create temporarily to get pascal name
            context = {
                "cookiecutter": {
                    "domain_name": domain_name,
                    "pascal_domain_name": domain_config.pascal_case_name,
                    "snake_domain_name": domain_name.replace("-", "_"),
                    "base_classes": settings.base_classes.model_dump(),
                    **context,
                }
            }

            console.print(f"Adding domain [bold blue]{domain_name}[/]...")
            try:
                template_engine.generate_project(
                    "domain", self.project_path / "src" / "domains", context
                )
                console.print(f"Domain added at [bold green]{domain_path}[/]")
            except Exception as e:
                raise ValueError(f"Failed to generate domain template: {e}")

            # Save updated configuration
            try:
                self._save_config()
            except Exception as e:
                raise ValueError(f"Failed to save project configuration: {e}")

            return domain_path

        except Exception as e:
            raise ValueError(str(e))

    def add_bounded_context(
        self,
        project_path: Union[str, Path],
        domain_name: str,
        context_name: str,
        context: Optional[Dict] = None,
    ) -> Path:
        """Add a new bounded context to a domain."""
        try:
            self.project_path = Path(project_path)
            if not self.project_path.exists():
                raise ValueError(f"Not a nagraj project: {project_path}")

            self.config = self._load_config(self.project_path)

            domain_path = self.project_path / "src" / "domains" / domain_name
            if not domain_path.exists():
                raise ValueError(f"Domain {domain_name} does not exist")

            context_path = domain_path / context_name
            if context_path.exists():
                raise ValueError(
                    f"Bounded context {context_name} already exists in domain {domain_name}"
                )

            # Create bounded context configuration
            bc_config = BoundedContextConfig(
                name=context_name,
                description=f"Bounded context for {context_name} in {domain_name} domain",
            )
            self.config.add_bounded_context(domain_name, bc_config)

            # Generate bounded context files
            context = context or {}
            context = {
                "cookiecutter": {
                    "domain_name": domain_name,
                    "context_name": context_name,
                    "base_classes": settings.base_classes.model_dump(),
                    **context,
                }
            }

            console.print(
                f"Adding bounded context [bold blue]{context_name}[/] to domain [bold blue]{domain_name}[/]..."
            )
            template_engine.generate_project("context", domain_path, context)
            console.print(f"Bounded context added at [bold green]{context_path}[/]")

            # Save updated configuration
            self._save_config()
            return context_path

        except Exception as e:
            raise ValueError(f"Failed to add bounded context: {e}")

    def add_entity(
        self,
        project_path: Union[str, Path],
        domain_name: str,
        context_name: str,
        entity_name: str,
        description: Optional[str] = None,
    ) -> Path:
        """Add a new entity to a bounded context.

        Args:
            project_path: Path to the project root directory.
            domain_name: Name of the domain containing the bounded context.
            context_name: Name of the bounded context to add the entity to.
            entity_name: Name of the entity to add.
            description: Optional description of the entity.

        Returns:
            Path to the created entity file.

        Raises:
            ValueError: If the project, domain, or bounded context does not exist.
        """
        try:
            self.project_path = Path(project_path)
            if not self.project_path.exists():
                raise ValueError(f"Not a nagraj project: {project_path}")

            # Load project configuration
            try:
                self.config = self._load_config(self.project_path)
            except ValueError as e:
                if "not a nagraj project" in str(e).lower():
                    raise
                raise ValueError(f"Failed to load project configuration: {e}")

            # Check if domain exists
            domain_path = self.project_path / "src" / "domains" / domain_name
            if not domain_path.exists():
                raise ValueError(f"Domain {domain_name} does not exist")

            # Check if bounded context exists
            context_path = domain_path / context_name
            if not context_path.exists():
                raise ValueError(
                    f"Bounded context {context_name} does not exist in domain {domain_name}"
                )

            # Check if entity directory exists
            entities_path = context_path / "domain" / "entities"
            if not entities_path.exists():
                raise ValueError(
                    f"Entities directory does not exist in bounded context {context_name}"
                )

            # Check if entity already exists
            entity_file = entities_path / f"{entity_name.replace('-', '_')}.py"
            if entity_file.exists():
                raise ValueError(
                    f"Entity {entity_name} already exists in bounded context {context_name}"
                )

            # Generate entity file
            context = {
                "cookiecutter": {
                    "entity_name": entity_name,
                    "pascal_entity_name": "".join(
                        part.capitalize()
                        for part in entity_name.replace("-", "_").split("_")
                    ),
                    "description": description,
                }
            }

            try:
                template_engine.write_template(
                    "entity/{{cookiecutter.entity_name}}.py",
                    entity_file,
                    context,
                )
                console.print(f"Entity file created at [bold]{entity_file}[/]")
            except Exception as e:
                raise ValueError(f"Failed to generate entity file: {e}")

            return entity_file

        except Exception as e:
            raise ValueError(str(e))


# Global project manager instance
project_manager = ProjectManager()
