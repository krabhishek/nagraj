"""Command to validate project structure."""

from pathlib import Path

import click
from click.exceptions import Exit
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from nagraj.core.project import project_manager

console = Console()


@click.command()
@click.option(
    "--project-dir",
    "-p",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path.cwd(),
    help="Project root directory",
)
def validate(project_dir: Path) -> None:
    """Validate project structure against DDD standards."""
    try:
        # Check if directory exists
        if not project_dir.exists():
            console.print(f"[bold red]Error:[/] Not a nagraj project: {project_dir}")
            raise Exit(code=1)

        # Load project configuration
        try:
            project_manager.project_path = project_dir
            project_manager.config = project_manager._load_config(project_dir)
        except ValueError as e:
            if "not a nagraj project" in str(e).lower():
                console.print(
                    f"[bold red]Error:[/] Not a nagraj project: {project_dir}"
                )
            else:
                console.print(f"[bold red]Error:[/] {str(e)}")
            raise Exit(code=1)

        # Validate structure
        errors = project_manager.config.validate_structure(str(project_dir))

        if not errors:
            console.print(
                Panel(
                    Text("✓ Project structure is valid", style="green bold"),
                    title="Validation Success",
                    border_style="green",
                )
            )
        else:
            # Show errors
            console.print("\n[bold red]Validation Errors:[/]")
            for error in errors:
                console.print(f"[red]• {error}[/]")
            raise Exit(code=1)

    except Exit:
        raise
    except Exception as e:
        console.print(f"[bold red]Error:[/] {str(e)}")
        raise Exit(code=1)
