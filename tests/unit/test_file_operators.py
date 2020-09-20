from redbaron import RedBaron

from plissken.documents.helpers import prettyDoc
from plissken.documents.package import PackageDoc
from plissken.file_operators import code2red, render_template


def test_code2red(test_code_file):
    """ test code to red baron"""

    rb = code2red(test_code_file)
    assert isinstance(rb, RedBaron)


def test_render_template(test_package_dir):

    template = render_template(
        "md.template", data=prettyDoc(PackageDoc(test_package_dir))
    )
    assert isinstance(template, str)


def test_render_external_template(template_dir):

    template = render_template(
        "external.template", data={"message": "works"}, directory=template_dir
    )
    assert template == "works"
