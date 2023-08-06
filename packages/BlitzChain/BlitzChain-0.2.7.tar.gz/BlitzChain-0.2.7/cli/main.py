"""Ingest data
"""
import click

@click.group()
def cli_interface():
    """My CLI tool"""
    pass

@click.command()
def insert_json():
    """Insert JSON"""
    click.echo("Executing command 1")

@click.command()
def insert_csv():
    """Command 2 description"""
    click.echo("Executing command 2")


cli_interface.add_command(insert_json)
cli_interface.add_command(insert_csv)

if __name__ == '__main__':
    cli_interface()
