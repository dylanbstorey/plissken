import os

from redbaron import RedBaron

from plissken.code_parser import VariableDoc, code2red


def test_code2red(test_code_file):
    """ test code to red baron"""

    rb = code2red(test_code_file)
    assert isinstance(rb, RedBaron)


def test_variable_doc(rb_variables):
    """ test the variable doc class """

    for node in rb_variables:

        doc_obj = VariableDoc(node[0], node[1])
        assert isinstance(doc_obj.docstring, str)
        assert isinstance(doc_obj.name, str)
        assert isinstance(doc_obj.type, str)
