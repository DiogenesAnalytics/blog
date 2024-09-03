"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Jupyter Blog Utilities."""


if __name__ == "__main__":
    main(prog_name="blog_utils")  # pragma: no cover
