from pathlib import Path
from typing import Dict, Optional, Union

from rich.console import Console

from nagraj.config.settings import ProjectConfig, settings
from nagraj.core.template import template_engine

console = Console()


class ProjectManager:
    """Manages project structure and modifications."""

    def create_project(
        self,
        name: str,
        output_dir: Union[str, Path],
        description: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Path:
        """Create a new project with the DDD structure."""
        config = ProjectConfig(name=name, description=description, author=author)

        context = {
            "project_name": name,
            "project_description": description or f"A DDD/CQRS project named {name}",
            "author": author or "Unknown",
            "python_version": config.python_version,
            "dependencies": config.dependencies,
            "base_classes": settings.base_classes.model_dump(),
        }

        console.print(f"Creating new project [bold blue]{name}[/]...")
        project_path = template_engine.generate_project("project", output_dir, context)
        console.print(f"Project created at [bold green]{project_path}[/]")
        return project_path

    def add_domain(
        self,
        project_path: Union[str, Path],
        domain_name: str,
        context: Optional[Dict] = None,
    ) -> Path:
        """Add a new domain to an existing project."""
        project_path = Path(project_path)
        domain_path = project_path / "src" / "domains" / domain_name

        if domain_path.exists():
            raise ValueError(f"Domain {domain_name} already exists")

        context = context or {}
        context.update(
            {
                "domain_name": domain_name,
                "base_classes": settings.base_classes.model_dump(),
            }
        )

        console.print(f"Adding domain [bold blue]{domain_name}[/]...")
        template_engine.generate_project(
            "domain", project_path / "src" / "domains", context
        )
        console.print(f"Domain added at [bold green]{domain_path}[/]")
        return domain_path

    def add_bounded_context(
        self,
        project_path: Union[str, Path],
        domain_name: str,
        context_name: str,
        context: Optional[Dict] = None,
    ) -> Path:
        """Add a new bounded context to a domain."""
        project_path = Path(project_path)
        domain_path = project_path / "src" / "domains" / domain_name

        if not domain_path.exists():
            raise ValueError(f"Domain {domain_name} does not exist")

        context_path = domain_path / context_name
        if context_path.exists():
            raise ValueError(
                f"Bounded context {context_name} already exists in domain {domain_name}"
            )

        context = context or {}
        context.update(
            {
                "domain_name": domain_name,
                "context_name": context_name,
                "base_classes": settings.base_classes.model_dump(),
            }
        )

        console.print(
            f"Adding bounded context [bold blue]{context_name}[/] to domain [bold blue]{domain_name}[/]..."
        )
        template_engine.generate_project("context", domain_path, context)
        console.print(f"Bounded context added at [bold green]{context_path}[/]")
        return context_path


# Global project manager instance
project_manager = ProjectManager()
