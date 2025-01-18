import click
from rich.console import Console

from nagraj.cli.commands.context import add_bounded_context
from nagraj.cli.commands.domain import add_domain
from nagraj.cli.commands.new import new

console = Console()


@click.group()
@click.version_option()
def cli():
    """Nagraj - A CLI tool for generating DDD/CQRS microservices applications."""
    pass


# Register commands
cli.add_command(new)
cli.add_command(add_domain)
cli.add_command(add_bounded_context)

if __name__ == "__main__":
    cli()
