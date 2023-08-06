import click
from file_finder.finder import finder
from file_finder.finder import FileFinderError

def cli():
    try:
        finder()
    except FileFinderError as err:
        click.echo(click.style(err, bg='black', fg='red', italic=True))