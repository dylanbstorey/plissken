import os

from redbaron import RedBaron


def code2red(filename: str) -> RedBaron:
    with open(filename) as sc:
        red = RedBaron(sc.read())
    return red
