from pathlib import Path

import click
from rich.console import Console

from nagraj.core.project import project_manager

console = Console()


@click.command(name="add-domain")
@click.argument("domain_name")
@click.option(
    "--project-dir",
    "-p",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=Path.cwd(),
    help="Project root directory",
)
def add_domain(domain_name: str, project_dir: Path) -> None:
    """Add a new domain to the project."""
    try:
        project_manager.add_domain(project_path=project_dir, domain_name=domain_name)
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        raise click.Abort()
