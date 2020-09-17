import os
import shutil

import pytest
import redbaron

import plissken


def pytest_itemcollected(item):
    """
    use test doc strings as messages for the testing suite
    :param item:
    :return:
    """
    if item._obj.__doc__:
        item._nodeid = item.obj.__doc__.strip()


HERE = os.path.dirname(__file__)
test_files = [os.path.join(HERE, "unit", "artifact", "example_google.py")]


@pytest.fixture()
def test_code_file():
    return test_files[0]


@pytest.fixture()
def get_rb():
    return plissken.code_parser.code2red(test_files[0])


@pytest.fixture()
def rb_variables():

    rv = []
    rb = plissken.code_parser.code2red(test_files[0])

    for ix, node in enumerate(rb):
        if isinstance(
            rb[ix],
            (
                redbaron.nodes.StandaloneAnnotationNode,
                redbaron.nodes.AssignmentNode,
                redbaron.nodes.NameNode,
            ),
        ):
            if isinstance(rb[ix + 1], redbaron.nodes.StringNode):
                rv.append((rb[ix], rb[ix + 1]))

    return rv


@pytest.fixture
def directories():
    """
    What does this fixture do ?
    :return:
    """

    dirs = [
        os.path.join("test_module"),
        os.path.join("test_module", "test1"),
        os.path.join("test_module", "test2"),
        os.path.join("test_module", "test3"),
    ]

    for d in dirs:
        os.makedirs(d, exist_ok=True)

    files = [os.path.join(d, "test.py") for d in dirs]
    files += [os.path.join(d, "__init__.py") for d in dirs]

    for f in files:
        open(f, "w")

    yield files, dirs

    for f in files:
        os.unlink(f)

    for d in dirs:
        try:
            shutil.rmtree(d)
        except FileNotFoundError:
            pass
