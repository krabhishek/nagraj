"""Remove commands for Nagraj."""

from pathlib import Path

import click
from click.exceptions import Exit
from rich.console import Console

from nagraj.core.project import project_manager

console = Console()


@click.group(name="remove")
def remove() -> None:
    """Remove components from your project."""
    pass


@remove.command(name="domain")
@click.argument("name")
@click.option(
    "--project-dir",
    "-p",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path.cwd(),
    help="Project root directory",
)
@click.option("--debug/--no-debug", default=False, help="Enable debug output")
def remove_domain(name: str, project_dir: Path, debug: bool = False) -> None:
    """Remove a domain from the project.

    NAME is the name of the domain to remove.
    """
    try:
        if debug:
            console.print(
                f"Debug: Removing domain {name} from project at {project_dir}"
            )

        # Check if project directory exists
        if not project_dir.exists():
            console.print(f"[red]Error:[/red] Directory {project_dir} does not exist")
            raise Exit(1)

        # Load project configuration
        try:
            project_manager.project_path = project_dir
            project_manager.config = project_manager._load_config(project_dir)
        except ValueError as e:
            if "not a nagraj project" in str(e).lower():
                console.print(f"[red]Error:[/red] Not a nagraj project: {project_dir}")
            else:
                console.print(f"[red]Error:[/red] {str(e)}")
            raise Exit(1)

        # Check if domain exists
        domain_path = project_dir / "src" / "domains" / name
        if not domain_path.exists():
            console.print(f"[red]Error:[/red] Domain {name} does not exist")
            raise Exit(1)

        # Remove domain from configuration
        project_manager.config.remove_domain(name)

        # Save updated configuration
        project_manager._save_config()

        # Remove domain directory
        import shutil

        shutil.rmtree(domain_path)

        console.print(f"[green]✓[/green] Removed domain '{name}' from project")

    except Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        if debug:
            console.print_exception()
        raise Exit(1)


@remove.command(name="bc")
@click.argument("domain_name")
@click.argument("context_name")
@click.option(
    "--project-dir",
    "-p",
    type=click.Path(file_okay=False, path_type=Path),
    default=Path.cwd(),
    help="Project root directory",
)
@click.option("--debug/--no-debug", default=False, help="Enable debug output")
def remove_bounded_context(
    domain_name: str, context_name: str, project_dir: Path, debug: bool = False
) -> None:
    """Remove a bounded context from a domain.

    DOMAIN_NAME is the name of the domain containing the bounded context.
    CONTEXT_NAME is the name of the bounded context to remove.
    """
    try:
        if debug:
            console.print(
                f"Debug: Removing bounded context {context_name} from domain {domain_name} "
                f"in project at {project_dir}"
            )

        # Check if project directory exists
        if not project_dir.exists():
            console.print(f"[red]Error:[/red] Directory {project_dir} does not exist")
            raise Exit(1)

        # Load project configuration
        try:
            project_manager.project_path = project_dir
            project_manager.config = project_manager._load_config(project_dir)
        except ValueError as e:
            if "not a nagraj project" in str(e).lower():
                console.print(f"[red]Error:[/red] Not a nagraj project: {project_dir}")
            else:
                console.print(f"[red]Error:[/red] {str(e)}")
            raise Exit(1)

        # Check if domain exists
        domain_path = project_dir / "src" / "domains" / domain_name
        if not domain_path.exists():
            console.print(f"[red]Error:[/red] Domain {domain_name} does not exist")
            raise Exit(1)

        # Check if bounded context exists
        context_path = domain_path / context_name
        if not context_path.exists():
            console.print(
                f"[red]Error:[/red] Bounded context {context_name} does not exist in domain {domain_name}"
            )
            raise Exit(1)

        # Remove bounded context from configuration
        project_manager.config.remove_bounded_context(domain_name, context_name)

        # Save updated configuration
        project_manager._save_config()

        # Remove bounded context directory
        import shutil

        shutil.rmtree(context_path)

        console.print(
            f"[green]✓[/green] Removed bounded context '{context_name}' from domain '{domain_name}'"
        )

    except Exit:
        raise
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}")
        if debug:
            console.print_exception()
        raise Exit(1)
