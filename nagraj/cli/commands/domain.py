"""Command to add a domain to a project."""

from pathlib import Path

import click
from click.exceptions import Exit
from rich.console import Console

from nagraj.core.project import project_manager

console = Console()


@click.command()
@click.argument("domain_name")
@click.option(
    "--project-dir",
    "-p",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path.cwd(),
    help="Project root directory",
)
@click.option("--debug/--no-debug", default=False, help="Enable debug output")
def add_domain(domain_name: str, project_dir: Path, debug: bool = False) -> None:
    """Add a new domain to the project."""
    try:
        if debug:
            console.print(
                f"Debug: Adding domain {domain_name} to project at {project_dir}"
            )

        # Add domain
        domain_path = project_manager.add_domain(project_dir, domain_name)
        console.print(
            f"\n[bold green]✓[/] Domain added successfully at [bold]{domain_path}[/]"
        )

    except ValueError as e:
        if "not a nagraj project" in str(e).lower():
            console.print(f"[bold red]Error:[/] Not a nagraj project: {project_dir}")
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
