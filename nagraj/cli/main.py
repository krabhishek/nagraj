"""Main CLI entry point."""

import click
from rich.console import Console

from nagraj.cli.commands.add import add
from nagraj.cli.commands.new import new
from nagraj.cli.commands.remove import remove
from nagraj.cli.commands.validate import validate

console = Console()


@click.group()
@click.version_option()
def cli():
    """Nagraj - A CLI tool for generating DDD/CQRS microservices applications."""
    pass


# Register commands
cli.add_command(new)
cli.add_command(add)
cli.add_command(remove)
cli.add_command(validate)

if __name__ == "__main__":
    cli()
