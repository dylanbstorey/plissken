from redbaron import RedBaron

import plissken
from plissken import generate_docs
from plissken.file_operators import code2red


def test_version():
    """test plissken version"""

    assert plissken.__version__


def test_code2red(test_code_file):
    """ test code to red baron"""

    rb = code2red(test_code_file)
    assert isinstance(rb, RedBaron)


def test_generate_docts(test_package_dir):
    generate_docs(test_package_dir)
