"""Command to initialize a new project using nagraj templates."""

import subprocess
from pathlib import Path
from typing import Optional

import click
from cookiecutter.main import cookiecutter
from rich.console import Console

from nagraj.core.logging import logger_service

console = Console()
logger = logger_service.get_logger()


def get_git_config_value(key: str) -> Optional[str]:
    """Get a value from git global config.

    Args:
        key: The git config key to retrieve

    Returns:
        The config value if found, None otherwise
    """
    try:
        result = subprocess.run(
            ["git", "config", "--global", "--get", key],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        logger.debug(f"Failed to get git config value for {key}")
        return None


@click.command()
@click.option(
    "--project-name",
    default="my_app",
    help="Name of the project (default: my_app)",
)
@click.option(
    "--project-root-dir",
    default=".",
    help="Root directory for the project (default: current directory)",
    type=click.Path(file_okay=False, dir_okay=True, path_type=Path),
)
@click.option(
    "--project-author-name",
    default=lambda: get_git_config_value("user.name") or "Noname",
    help="Project author name (default: git global user.name or 'Noname')",
)
@click.option(
    "--project-author-email",
    default=lambda: get_git_config_value("user.email") or "noemail@example.com",
    help="Project author email (default: git global user.email or 'noemail@example.com')",
)
@click.option(
    "--project-description",
    default="A Python project generated using nagraj",
    help="Short description of the project",
)
@click.option(
    "--python-version",
    default="3.12",
    help="Python version to use (default: 3.12)",
)
@click.option(
    "--version",
    default="0.1.0",
    help="Initial version of the project (default: 0.1.0)",
)
def init(
    project_name: str,
    project_root_dir: Path,
    project_author_name: str,
    project_author_email: str,
    project_description: str,
    python_version: str,
    version: str,
) -> None:
    """Initialize a new Python project using nagraj templates.

    This command creates a new Python project using the nagraj-full-project-template.
    It sets up the basic project structure following best practices and includes
    all necessary configuration files.
    """
    try:
        logger.info(
            "Initializing new project",
            project_name=project_name,
            project_root_dir=str(project_root_dir),
            author=project_author_name,
        )

        # Get the absolute path to the template directory
        template_dir = (
            Path(__file__).parent.parent.parent
            / "templates"
            / "nagraj-full-project-template"
        )

        # Ensure the template directory exists
        if not template_dir.exists():
            logger.error(f"Template directory not found: {template_dir}")
            raise click.ClickException(f"Template directory not found: {template_dir}")

        logger.debug("Using template directory", template_dir=str(template_dir))

        # Create the project using cookiecutter
        logger.info("Generating project from template")
        cookiecutter(
            str(template_dir),
            output_dir=str(project_root_dir),
            no_input=True,
            extra_context={
                "project_name": project_name,
                "author_name": project_author_name,
                "author_email": project_author_email,
                "project_description": project_description,
                "python_version": python_version,
                "version": version,
            },
        )

        logger.success(
            "Project created successfully",
            project_name=project_name,
            location=str(project_root_dir / project_name),
        )
        console.print(f"✨ Successfully created project [bold green]{project_name}[/]")
        console.print(f"📁 Project location: {project_root_dir / project_name}")

    except Exception as e:
        logger.error(
            "Failed to create project",
            error=str(e),
            project_name=project_name,
            project_root_dir=str(project_root_dir),
        )
        raise click.ClickException(f"Failed to create project: {str(e)}")
