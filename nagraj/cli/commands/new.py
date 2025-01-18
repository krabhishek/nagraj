from pathlib import Path
from typing import Optional

import click
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
def new(
    name: str,
    output_dir: Path,
    description: Optional[str] = None,
    author: Optional[str] = None,
) -> None:
    """Create a new DDD/CQRS project."""
    try:
        project_manager.create_project(
            name=name, output_dir=output_dir, description=description, author=author
        )
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        raise click.Abort()
