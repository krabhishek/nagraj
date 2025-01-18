"""Add commands for Nagraj."""

from pathlib import Path
from typing import Optional

import click
from click.exceptions import Exit
from rich.console import Console

from nagraj.config.schema import DomainConfig, DomainType
from nagraj.core.project import ProjectManager, project_manager

console = Console()


@click.group(name="add")
def add():
    """Add components to your project."""
    pass


@add.command(name="domain")
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


@add.command(name="bc")
@click.argument("domain_name")
@click.argument("context_name")
@click.option(
    "--project-dir",
    "-p",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=Path.cwd(),
    help="Project root directory",
)
@click.option("--debug/--no-debug", default=False, help="Enable debug output")
def add_bounded_context(
    domain_name: str, context_name: str, project_dir: Path, debug: bool = False
) -> None:
    """Add a new bounded context to a domain."""
    try:
        if debug:
            console.print(
                f"Debug: Adding bounded context {context_name} to domain {domain_name} "
                f"in project at {project_dir}"
            )

        # Add bounded context
        context_path = project_manager.add_bounded_context(
            project_dir, domain_name, context_name
        )
        console.print(
            f"\n[bold green]✓[/] Bounded context added successfully at [bold]{context_path}[/]"
        )

    except ValueError as e:
        if "already exists" in str(e).lower():
            console.print(
                f"[bold red]Error:[/] Bounded context already exists: {context_name}"
            )
        else:
            console.print(f"[bold red]Error:[/] {str(e)}")
        if debug:
            import traceback

            console.print("[red]Debug traceback:[/]")
            console.print(traceback.format_exc())
        raise Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Error:[/] An unexpected error occurred: {str(e)}")
        if debug:
            import traceback

            console.print("[red]Debug traceback:[/]")
            console.print(traceback.format_exc())
        raise Exit(code=1)
