"""
    plissken.cli
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    plissken's command line interface

"""

import click


@click.group()
def main():
    """
    The main entry point for plissken
    :return:
    """
    pass


@main.command()
def subcommand():
    """
    This is a sub command on the main entry point group
    :return:
    """
    pass