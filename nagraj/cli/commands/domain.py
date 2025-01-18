"""Command to add a domain to a project."""

from pathlib import Path
from typing import Optional

import click
from click.exceptions import Exit
from rich.console import Console

from nagraj.config.schema import DomainConfig, DomainType
from nagraj.core.project import ProjectManager

console = Console()


@click.command("add-domain")
@click.argument("name")
@click.option(
    "--project-dir",
    "-p",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path.cwd(),
    help="Project root directory",
)
@click.option(
    "--type",
    "-t",
    type=click.Choice([t.value for t in DomainType], case_sensitive=False),
    default=DomainType.CORE.value,
    help="Type of domain",
)
@click.option(
    "--description",
    "-d",
    help="Description of the domain",
)
@click.option(
    "--debug/--no-debug",
    default=False,
    help="Enable debug output",
)
def add_domain(
    name: str,
    project_dir: Path,
    type: str,
    description: Optional[str],
    debug: bool,
) -> None:
    """Add a domain to the project.

    NAME is the name of the domain to add. It should be in kebab-case format
    (e.g., 'order' or 'order-management') and should be singular.
    """
    try:
        # Validate domain name
        is_valid, error = DomainConfig.validate_domain_name(name)
        if not is_valid:
            console.print(f"[red]Error:[/red] {error}")
            raise Exit(1)

        # Create domain config
        domain_config = DomainConfig(
            name=name,
            type=DomainType(type),
            description=description,
        )

        # Create project manager and add domain
        project = ProjectManager()
        try:
            domain_path = project.add_domain(
                project_dir,
                name,
                {
                    "description": description,
                    "type": type,
                },
            )
            console.print(
                f"[green]✓[/green] Added domain '{name}' to project at {domain_path}"
            )
        except ValueError as e:
            if "not a nagraj project" in str(e).lower():
                console.print(f"[red]Error:[/red] Not a nagraj project: {project_dir}")
            else:
                console.print(f"[red]Error:[/red] {str(e)}")
            raise Exit(1)

    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        if debug:
            console.print_exception()
        raise Exit(1)
