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
def generate():
    """
    This is a sub command on the main entry point group
    :return:
    """
    # given directory
    # given template + template dir
    # given type (default markdown)
    # parse to a single package object
    #

    pass
