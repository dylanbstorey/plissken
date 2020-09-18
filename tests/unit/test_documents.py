import plissken
import plissken.documents.package
from plissken.documents.function import (
    FunctionDoc,
    _generate_arguments,
    _generate_decorators,
)
from plissken.documents.klass import ClassDoc
from plissken.documents.module import ModuleDoc
from plissken.documents.package import PackageDoc
from plissken.documents.variable import VariableDoc


def test_variable_doc(rb_variables):
    """ test the variable doc class """

    for node in rb_variables:

        doc_obj = VariableDoc(node[0], node[1])
        assert isinstance(doc_obj, plissken.documents.variable.VariableDocument)
        assert isinstance(doc_obj.docstring, str)
        assert isinstance(doc_obj.name, str)
        assert isinstance(doc_obj.annotation, str)


def test_decorator_generator(rb_decorated_functions):
    """ test ability to parse decorators """

    for decorated_function in rb_decorated_functions:
        decorator = _generate_decorators(decorated_function)
        for d in decorator:
            assert isinstance(d, plissken.documents.function.DecoratorDocument)


def test_function_argument_generator(rb_functions_with_args):
    """ test ability to parse functions """

    for function in rb_functions_with_args:
        arguments = _generate_arguments(function)
        for argument in arguments:
            assert isinstance(argument, plissken.documents.function.ArgumentDocument)


def test_function_doc(rb_functions):
    """ test function doc generation """

    for function in rb_functions:
        function = FunctionDoc(function)
        assert isinstance(function, plissken.documents.function.FunctionDocument)


def test_class_doc(rb_classes):

    for klass in rb_classes:
        klass = ClassDoc(klass)
        assert isinstance(klass, plissken.documents.klass.ClassDocument)


def test_module_doc(test_code_file):
    module = ModuleDoc(test_code_file)
    assert isinstance(module, plissken.documents.module.ModuleDocument)


def test_package_doc(test_package_dir):
    package = PackageDoc(test_package_dir)
    assert isinstance(package, plissken.documents.package.PackageDocument)
