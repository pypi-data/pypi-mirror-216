"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """GridWorks Price Service."""


if __name__ == "__main__":
    main(prog_name="gridworks-ps")  # pragma: no cover
