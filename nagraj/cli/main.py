"""Main CLI entry point."""

import click
from rich.console import Console

from nagraj.cli.commands import init

console = Console()


@click.group()
@click.version_option()
def cli() -> None:
    """Nagraj - A CLI tool for generating DDD/CQRS microservices applications."""
    pass


# Register commands
cli.add_command(init)


if __name__ == "__main__":
    cli()
