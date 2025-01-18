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
@click.option(
    "--domain",
    help="Initial domain name (defaults to 'core')",
    default="core",
)
@click.option(
    "--context",
    help="Initial bounded context name (defaults to 'main')",
    default="main",
)
@click.option("--debug/--no-debug", default=False, help="Enable debug output")
def new(
    name: str,
    output_dir: Path,
    description: Optional[str] = None,
    author: Optional[str] = None,
    domain: str = "core",
    context: str = "main",
    debug: bool = False,
) -> None:
    """Create a new DDD/CQRS project with initial domain and bounded context.

    NAME is the name of the project to create.
    """
    try:
        if debug:
            console.print(
                f"Debug: Creating project with name={name}, output_dir={output_dir}, "
                f"description={description}, author={author}, domain={domain}, context={context}"
            )

        # Create project
        project_path = project_manager.create_project(
            name=name,
            output_dir=output_dir,
            description=description,
            author=author,
        )

        # Add initial domain
        try:
            domain_path = project_manager.add_domain(
                project_path,
                domain,
                {
                    "description": f"Initial domain for {name} project",
                    "type": "core",
                },
            )
            console.print(
                f"[green]✓[/green] Added initial domain '{domain}' at {domain_path}"
            )

            # Add initial bounded context
            context_path = project_manager.add_bounded_context(
                project_path, domain, context
            )
            console.print(
                f"[green]✓[/green] Added initial bounded context '{context}' at {context_path}"
            )

        except Exception as e:
            console.print(
                f"[red]Error:[/red] Failed to create initial structure: {str(e)}"
            )
            raise Exit(1)

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
