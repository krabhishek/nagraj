"""Command to create a new project."""

from pathlib import Path
from typing import Optional

import click
from click.exceptions import Exit
from rich.console import Console

from nagraj.core.project import project_manager

console = Console()


@click.command()
@click.argument("name")
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path.cwd(),
    help="Directory where the project will be created",
)
@click.option("--description", "-d", help="Project description")
@click.option("--author", "-a", help="Project author")
@click.option("--debug/--no-debug", default=False, help="Enable debug output")
def new(
    name: str,
    output_dir: Path,
    description: Optional[str] = None,
    author: Optional[str] = None,
    debug: bool = False,
) -> None:
    """Create a new DDD/CQRS project."""
    try:
        if debug:
            console.print(
                f"Debug: Creating project with name={name}, output_dir={output_dir}, "
                f"description={description}, author={author}"
            )

        # Create project
        project_path = project_manager.create_project(
            name=name,
            output_dir=output_dir,
            description=description,
            author=author,
        )

        # Print success message
        console.print(
            f"\n[bold green]✓[/] Project created successfully at [bold]{project_path}[/]"
        )

    except ValueError as e:
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
