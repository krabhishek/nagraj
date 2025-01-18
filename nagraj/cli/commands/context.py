"""Command to add a bounded context to a domain."""

from pathlib import Path

import click
from click.exceptions import Exit
from rich.console import Console

from nagraj.core.project import project_manager

console = Console()


@click.command(name="add-bc")
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
