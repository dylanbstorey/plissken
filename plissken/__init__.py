"""plissken
"""
import os
import typing

__version__ = (
    open(os.path.join(os.path.dirname(__file__), "VERSION"), "r").read().strip()
)


def split_all(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path:  # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


def module_to_fqdns(
    folder: str
) -> typing.Tuple[typing.List[str], typing.List[str], typing.List[str]]:

    paths = []
    fqdns = []
    outputs = []

    for root, dirs, files in os.walk(folder):
        for f in files:
            paths.append(os.path.join(root, f))
            if f == "__init__.py":
                fqdns.append(".".join(split_all(root)))
                outputs.append(os.path.join(*split_all(root), "index"))
            else:
                fqdns.append(".".join(split_all(root) + [f[:-3]]))
                outputs.append(os.path.join(*split_all(root), f[:-3]))

    return paths, fqdns, outputs
