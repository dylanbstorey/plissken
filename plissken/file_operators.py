import os

from redbaron import RedBaron


def code2red(filename: str) -> RedBaron:
    with open(filename) as sc:
        red = RedBaron(sc.read())
    return red


def get_qualified_name_from_path(file: str) -> str:
    base_name = os.path.basename(file)
    if base_name == "__init__.py":
        base_name = os.path.dirname(file)

    else:
        base_name = base_name[:-3]

    base_name = ".".join(os.path.split(base_name))

    if base_name.startswith("."):
        base_name = base_name[1:]

    return base_name
