from pathlib import Path

import click
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
def add_bounded_context(domain_name: str, context_name: str, project_dir: Path) -> None:
    """Add a new bounded context to a domain."""
    try:
        project_manager.add_bounded_context(
            project_path=project_dir, domain_name=domain_name, context_name=context_name
        )
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        raise click.Abort()
