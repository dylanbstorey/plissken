import os

from redbaron import RedBaron

import plissken
from plissken import (
    FunctionDoc,
    VariableDoc,
    _generate_arguments,
    _generate_decorators,
    code2red,
)


def test_version():
    """test plissken version"""

    assert plissken.__version__


def test_module_to_fqdn(directories):
    d = directories

    module = "test_module"
    files = [
        "test_module/test.py",
        "test_module/test1/test.py",
        "test_module/test2/test.py",
        "test_module/test3/test.py",
        "test_module/__init__.py",
        "test_module/test1/__init__.py",
        "test_module/test2/__init__.py",
        "test_module/test3/__init__.py",
    ]
    fqdns = [
        "test_module.test",
        "test_module.test1.test",
        "test_module.test2.test",
        "test_module.test3.test",
        "test_module",
        "test_module.test1",
        "test_module.test2",
        "test_module.test3",
    ]
    outputs = [
        "test_module/test",
        "test_module/test1/test",
        "test_module/test2/test",
        "test_module/test3/test",
        "test_module/index",
        "test_module/test1/index",
        "test_module/test2/index",
        "test_module/test3/index",
    ]

    return_struct = zip(files, fqdns)
    r_files, r_fqdns, r_outputs = plissken.module_to_fqdns("test_module")

    files.sort()
    fqdns.sort()
    r_fqdns.sort()
    r_files.sort()
    outputs.sort()
    r_outputs.sort()

    assert r_files == files
    assert r_fqdns == fqdns
    assert r_outputs == outputs


def test_code2red(test_code_file):
    """ test code to red baron"""

    rb = code2red(test_code_file)
    assert isinstance(rb, RedBaron)


def test_variable_doc(rb_variables):
    """ test the variable doc class """

    for node in rb_variables:

        doc_obj = VariableDoc(node[0], node[1])
        assert isinstance(doc_obj, plissken.VariableDocument)
        assert isinstance(doc_obj.docstring, str)
        assert isinstance(doc_obj.name, str)
        assert isinstance(doc_obj.annotation, str)


def test_decorator_generator(rb_decorated_functions):
    """ test ability to parse decorators """

    for decorated_function in rb_decorated_functions:
        decorator = _generate_decorators(decorated_function)
        for d in decorator:
            assert isinstance(d, plissken.DecoratorDocument)


def test_function_argument_generator(rb_functions_with_args):
    """ test ability to parse functions """

    for function in rb_functions_with_args:
        arguments = _generate_arguments(function)
        for argument in arguments:
            assert isinstance(argument, plissken.ArgumentDocument)


def test_function_doc(rb_functions):
    """ test function doc generation """

    for function in rb_functions:
        function = FunctionDoc(function)
        assert isinstance(function, plissken.FunctionDocument)
