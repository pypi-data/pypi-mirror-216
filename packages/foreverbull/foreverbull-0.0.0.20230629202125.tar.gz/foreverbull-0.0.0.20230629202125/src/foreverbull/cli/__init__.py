import typer

from .algo import algo
from .service import service

cli = typer.Typer()

cli.add_typer(algo, name="algo")
cli.add_typer(service, name="service")
